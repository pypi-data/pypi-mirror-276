"""
This file contains classes and methods for option pricing and analysis, utilizing various financial models and numerical methods. 
It allows for calculations of option Greeks and prices either using tree methods or finite difference methods among others. 
It supports both European and American options for price calculation.
Classes:
- Greeks: Calculate option Greeks (Delta, Gamma, Vega, etc.) using the Black-Scholes formula.
- OptionPricing: Main class for option pricing that utilizes different numerical methods and models including GARCH for volatility modeling.
The design favors flexibility in choosing pricing methods and models, offering tools for both simple and advanced option pricing scenarios.
"""
from stockdatamanager.customerrors import MethodError
from .datafetcher import Fetcher
from .utils import _SMA, _EMA, _SARIMAX_model
import pandas as pd
import numpy as np
import yfinance as yf
import re
from typing import Union
from scipy.stats import norm
from scipy import linalg
from scipy.stats import linregress
import matplotlib.pyplot as plt
import seaborn as sns
import arch
import optuna
import math
from abc import ABC, abstractmethod
import sys

class Greeks(object):
  """
  Class to calculate the greeks for an option
  Inputs:
  - ticker: str, the ticker of the stock
  - call: bool, whether the option is a call or a put
  - identification: Union[str, int], the contract symbol of the option or the index of the option in the option chain
                                     Note: to find the contract identifier, it is written as ticker-YY-MM-DD-C(or P)-strike price (omit the - and the strike price is in a thousands format, so 1000 is $1.00)
  - verbose: int, the verbosity of the output
  """
  def __init__(self, 
               ticker: str,
               call: bool,
               identification: Union[str, int],
               verbose: bool = False):
    self.fetcher = Fetcher(ticker)
    self.df, self.yf_ticker = self.fetcher.df, self.fetcher.yf_stock
    if type(identification) == str:
     self.option_chain = self.yf_ticker.option_chain().calls if call else self.yf_ticker.option_chain().puts
     self.option = self.option_chain[self.option_chain['contractSymbol'] == identification]
    elif type(identification) == int:
      self.option = self.yf_ticker.option_chain().calls.iloc[identification] if call else self.yf_ticker.option_chain().puts.iloc[identification]
    else:
      raise ValueError('identification must be either a string or an integer')
    self.verbose = verbose
    self.date = self.calculate_expiration()
    self.call = call

  def from_name_to_datestr(self, s: str) -> str:
    """Helper function to convert the contract symbol to a date string"""
    if self.verbose:
      print(f"Processing {s}")
    match = re.search(r'[A-Za-z](\d{2})(\d{2})(\d{2})[CP]', s)
    if match:
        year, month, day = match.groups()
        return f"20{year}-{month}-{day}"
    else:
        return "No date found"
  
  def calculate_expiration(self) -> pd.Timestamp:
    """Function to calculate the expiration date of the option"""
    if self.verbose:
      print("Calculating expiration date")
    to_process = self.option['contractSymbol']
    date_str = self.from_name_to_datestr(to_process)
    date = pd.to_datetime(date_str)
    return date

  def calculate_delta(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the delta of the option fed into the class, using the Black-Scholes formula.
    The delta is calculated as the first derivative of the option price with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating delta")
    option = self.option
    dataframe = self.df
    if self.call:
      S = dataframe['Close'].iloc[-1]
      K = option['strike']
      ##convert self.date to days until expiration
      T = (self.date - pd.to_datetime('today')).days / 365
      r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
      sigma = option['impliedVolatility']
      d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
      delta = norm.cdf(d1)
      return delta
    else:
      S = dataframe['Close'].iloc[-1]
      K = option['strike']
      T = (self.date - pd.to_datetime('today')).days / 365
      r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
      sigma = option['impliedVolatility']
      d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
      delta = norm.cdf(d1) - 1
      return delta
    
  def calculate_gamma(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the gamma of the option fed into the class, using the Black-Scholes formula.
    The gamma is calculated as the second derivative of the option price with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating gamma")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma
  
  def calculate_vega(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the vega of the option fed into the class, using the Black-Scholes formula.
    The vega is calculated as the first derivative of the option price with respect to the implied volatility.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating vega")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega
  
  def calculate_vanna(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the vanna of the option fed into the class, using the Black-Scholes formula.
    The vanna is calculated as the first derivative of the delta with respect to the implied volatility.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating vanna")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    vanna = -norm.pdf(d1) * d1 / sigma
    return vanna
  
  def calculate_theta(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the theta of the option fed into the class, using the Black-Scholes formula.
    The theta is calculated as the first derivative of the option price with respect to time.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating theta")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    dividends = self.fetcher.get_dividend_yield()
    r_adj = r - dividends
    d1 = (np.log(S / K) + (r_adj + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if self.call:
        theta = - (S * sigma * norm.pdf(d1)) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        theta = - (S * sigma * norm.pdf(d1)) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)    
    theta_per_day = theta / 365
    return theta_per_day
  
  def calculate_rho(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the rho of the option fed into the class, using the Black-Scholes formula.
    The rho is calculated as the first derivative of the option price with respect to the risk-free rate.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating rho")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if self.call:
      rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
      rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    return rho
  
  def calculate_vomma(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the vomma of the option fed into the class, using the Black-Scholes formula.
    The vomma is calculated as the second derivative of the option price with respect to the implied volatility.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating vomma")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    vomma = S * np.sqrt(T) * norm.pdf(d1) * (d1 * d2) / sigma
    return vomma
  
  def calculate_charm(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the charm of the option fed into the class, using the Black-Scholes formula.
    The charm is calculated as the first derivative of the delta with respect to time.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating charm")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    charm = -norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma * np.sqrt(T))
    return charm
  
  def calculate_speed(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the speed of the option fed into the class, using the Black-Scholes formula.
    The speed is calculated as the third derivative of the option price with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating speed")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    speed = -norm.pdf(d1) / (S ** 2 * sigma * np.sqrt(T)) * (d1 + sigma * np.sqrt(T))
    return speed
  
  def calculate_zomma(self, risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the zomma of the option fed into the class, using the Black-Scholes formula.
    The zomma is calculated as the derivative of the gamma with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating zomma")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    zomma = norm.pdf(d1) * (d1 * d2 - 1) / (S * sigma ** 2 * np.sqrt(T))
    return zomma
  
  def calculate_color(self, risk_free_rate_horizon: 'str' = '13 weeks') -> float:
    """
    Method to calculate the color of the option fed into the class, using the Black-Scholes formula.
    The color is calculated as the second derivative of the charm with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating color")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    color = -norm.pdf(d1) * (2 * r * T - d2 * sigma * np.sqrt(T)) / (2 * T * sigma**2 * np.sqrt(T))
    return color

  def calculate_ultima(self, risk_free_rate_horizon: 'str' = '13 weeks') -> float:
    """
    Method to calculate the ultima of the option fed into the class, using the Black-Scholes formula.
    The ultima is calculated as the second derivative of the vomma with respect to the price of the underlying asset.
    Inputs:
    - risk_free_rate_horizon: str, the horizon of the risk free rate
    """
    if self.verbose:
      print("Calculating ultima")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]
    K = option['strike']
    T = (self.date - pd.to_datetime('today')).days / 365
    r = self.fetcher.get_risk_free_rate(risk_free_rate_horizon)['Close'].iloc[-1]
    sigma = option['impliedVolatility']
    d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    ultima = S * np.sqrt(T) * norm.pdf(d1) * (d1 * d2 * (1 - d1 * d2) + d1 ** 2 + d2 ** 2) / sigma ** 2
    return ultima
  
  def calculate_lambda(self,risk_free_rate_horizon: str = '13 weeks') -> float:
    """
    Method to calculate the lambda (leverage) of the option fed into the class.
    Lambda is calculated as the product of Delta and the ratio of the underlying asset's price to the option's price.
    """
    if self.verbose:
        print("Calculating lambda")
    option = self.option
    dataframe = self.df
    S = dataframe['Close'].iloc[-1]  
    V = option['lastPrice'] 
    delta = self.calculate_delta(risk_free_rate_horizon)  
    lambda_ = delta * (S / V)
    return lambda_

class Option(object):
  def __init__(self, S, K, r, T, N, pu, pd_, div, sigma, call=True, american=False, verbose = False):
    """
    Inputs:
    - S: float, the price of the underlying asset
    - K: float, the strike price of the option
    - r: float, the risk-free rate
    - T: float, the time to expiration of the option
    - N: int, the number of time steps
    - pu: float, the probability at the up state
    - pd_: float, the probability at the down state
    - div: float, the dividend yield
    - sigma: float, the volatility of the underlying asset
    - call: bool, whether the option is a call or a put
    - american: bool, whether the option is American or European
    - verbose: bool, the verbosity of the output
    Internal class to implement all the tree methods for option pricing
    Please do not use this class, it is for internal use only (I know, I should have put a _ in the name, but I didn't, so please don't use it)
    """
    self.S = S
    self.K = K
    self.r = r
    self.T = T
    self.N = max(1, N)
    self.STs = [] 
    self.pu, self.pd_= pu, pd_
    self.div = div
    self.sigma = sigma
    self.is_call = call
    self.is_european = not american
    self.verbose = verbose

  @property
  def dt(self) -> float:
    """ Single time step, in years """
    return self.T / float(self.N)

  @property
  def df(self) -> float:
    """ The discount factor """
    return math.exp(-(self.r - self.div) * self.dt)  

class _FiniteDifferences(object):
  def __init__(self, S, K, r, T, sigma, Smax, M, N, call, verbose = False):
    """
    Inputs:
    - S: float, the price of the underlying asset
    - K: float, the strike price of the option
    - r: float, the risk-free rate
    - T: float, the time to expiration of the option
    - sigma: float, the volatility of the underlying asset
    - Smax: float, the maximum price of the underlying asset
    - M: int, the number of price steps
    - N: int, the number of time steps
    - call: bool, whether the option is a call or a put
    - verbose: bool, the verbosity of the output
    Internal class to implement the Finite Difference Method for option pricing
    Please do not use this class, it is for internal use only (I know, I should have put a _ in the name, but I didn't, so please don't use it)
    """
    self.S = S
    self.K = K
    self.r = r
    self.T = T
    self.sigma = sigma
    self.Smax = Smax
    self.M, self.N = M, N
    self.is_call = call
    self.i_values = np.arange(self.M)
    self.j_values = np.arange(self.N)
    self.grid = np.zeros(shape=(self.M + 1, self.N + 1))
    self.boundary_conds = np.linspace(0, Smax, self.M+1)
    self.verbose = verbose

  @property
  def dS(self) -> float:
    """  Single step in S space"""
    return self.Smax / float(self.M)

  @property
  def dt(self) -> float:
    """" Single step in t space"""
    return self.T / float(self.N)

  @abstractmethod
  def setup_boundary_conditions(self):
    raise NotImplementedError('This method is implemented in the subclasses')

  @abstractmethod
  def setup_coefficients(self):
    raise NotImplementedError('This method is implemented in the subclasses')

  @abstractmethod
  def traverse_grid(self):
    raise NotImplementedError("This method is implemented in the subclasses")
  @abstractmethod

  def interpolate(self) -> float:
    """
    Use piecewise linear interpolation on the initial grid column to get the closest price at S.
    """
    if self.verbose: print("Interpolating the option price")
    return np.interp(self.S, self.boundary_conds, self.grid[:,0])

  def price(self) -> float:
    """ Entry point of the pricing method"""
    if self.verbose: print("Pricing the option")
    self.setup_boundary_conditions()
    self.setup_coefficients()
    self.traverse_grid()
    return self.interpolate()

class _FDEU(_FiniteDifferences):
  """
  Class to implement the Explicit Finite Difference Method for option pricing,
  Meant for internal use only
  """
  def setup_boundary_conditions(self):
    """Setup the boundary conditions for the option pricing problem"""
    if self.verbose: print("Setting up boundary conditions")
    if self.is_call:
      self.grid[:,-1] = np.maximum(0, self.boundary_conds - self.K)
      self.grid[-1,:-1] = (self.Smax-self.K) * np.exp(-self.r*self.dt*(self.N - self.j_values))
    else:
      self.grid[:,-1] = np.maximum(0, self.K-self.boundary_conds)
      self.grid[0,:-1] = (self.K-self.Smax) * np.exp(-self.r*self.dt*(self.N-self.j_values))
    if self.verbose: print("Boundary conditions set")

  def setup_coefficients(self):
    """Setup the coefficients for the finite difference scheme"""
    if self.verbose: print("Setting up coefficients")
    self.a = 0.5 * self.dt * ((self.sigma ** 2) * (self.i_values ** 2) - self.r * self.i_values)
    self.b = 1 - self.dt * ((self.sigma ** 2) *(self.i_values ** 2) + self.r)
    self.c = 0.5 * self.dt * ((self.sigma ** 2) * (self.i_values ** 2) + self.r * self.i_values)
    if self.verbose: print("Coefficients set")

  def traverse_grid(self):
    """Function to iterate the grid backwards in time"""
    if self.verbose: print("Traversing the grid")
    for j in reversed(self.j_values):
      for i in range(self.M)[2:]:
        self.grid[i,j] = self.a[i]*self.grid[i-1,j+1] + self.b[i]*self.grid[i,j+1] + self.c[i]*self.grid[i+1,j+1]
    if self.verbose: print("Grid traversed")
                  
class _FDImpEU(_FDEU):
  """
  Internal class to implement the Implicit Finite Difference Method for option pricing
  """
  def setup_coefficients(self):
    """Setup the coefficients for the implicit finite difference scheme"""
    if self.verbose: print("Setting up coefficients")
    self.a = 0.5 * (self.r * self.dt * self.i_values - (self.sigma ** 2) * self.dt * (self.i_values ** 2))
    self.b = 1 + (self.sigma ** 2) * self.dt * (self.i_values ** 2) + self.r * self.dt
    self.c = -0.5 * (self.r * self.dt * self.i_values + (self.sigma ** 2) * self.dt * (self.i_values ** 2))
    self.coeffs = np.diag(self.a[2:self.M],-1) + np.diag(self.b[1:self.M]) + np.diag(self.c[1:self.M-1],1)
    if self.verbose: print("Coefficients set")

  def traverse_grid(self):
    """ Solve using linear systems of equations """
    if self.verbose: print("Traversing the grid")
    P, L, U = linalg.lu(self.coeffs)
    aux = np.zeros(self.M-1)
    for i in reversed(range(self.N)):
      aux[0] = np.dot(-self.a[1], self.grid[0, i])
      x1 = linalg.solve(L, self.grid[1:self.M, i+1]+aux)
      x2 = linalg.solve(U, x1)
      self.grid[1:self.M, i] = x2
    if self.verbose: print("Grid traversed")

class _FDCN(_FDEU):
  """Internal class to implement the Crank-Nicolson Finite Difference Method for option pricing"""
  def setup_coefficients(self):
    """Setup the coefficients for the Crank-Nicolson scheme"""
    if self.verbose: print("Setting up coefficients")
    self.alpha = 0.25 * self.dt * ((self.sigma ** 2) * (self.i_values ** 2) - self.r * self.i_values)
    self.beta = -self.dt * 0.5 * ((self.sigma ** 2) * (self.i_values ** 2) + self.r)
    self.gamma = 0.25 * self.dt * ((self.sigma ** 2) * (self.i_values ** 2) + self.r * self.i_values)
    self.M1 = -np.diag(self.alpha[2:self.M], -1) + np.diag(1-self.beta[1:self.M]) - np.diag(self.gamma[1:self.M-1], 1)
    self.M2 = np.diag(self.alpha[2:self.M], -1) + np.diag(1+self.beta[1:self.M]) + np.diag(self.gamma[1:self.M-1], 1)
    if self.verbose: print("Coefficients set")
  
  def traverse_grid(self):
    """ Solve using linear systems of equations """
    if self.verbose: print("Traversing the grid")
    P, L, U = linalg.lu(self.M1)
    for j in reversed(range(self.N)):
      x1 = linalg.solve(L, np.dot(self.M2, self.grid[1:self.M, j+1]))
      x2 = linalg.solve(U, x1)
      self.grid[1:self.M, j] = x2
    if self.verbose: print("Grid traversed")

class _FDCNUS(_FDCN):
  """Internal class to implement the Crank-Nicolson Finite Difference Method for american option pricing"""
  def __init__(self, S, K, r, T, sigma, Smax, M, N, omega, tol, call, verbose = False):
    super(_FDCNUS, self).__init__(S, K, r=r, T=T, sigma=sigma, Smax=Smax, M=M, N=N, call=call, verbose=verbose)
    self.omega = omega
    self.tol = tol
    self.i_values = np.arange(self.M+1)
    self.j_values = np.arange(self.N+1)

  def setup_boundary_conditions(self):
    """Setup the boundary conditions for the option pricing problem"""
    if self.verbose: print("Setting up boundary conditions")
    if self.is_call:
      self.payoffs = np.maximum(0, self.boundary_conds[1:self.M] - self.K)
    else:
      self.payoffs = np.maximum(0, self.K - self.boundary_conds[1:self.M])
    self.past_values = self.payoffs
    self.boundary_values = self.K * np.exp(-self.r * self.dt * (self.N - self.j_values))
    if self.verbose: print("Boundary conditions set")
        
  def calculate_payoff_start_boundary(self, rhs, old_values):
    """Calculate the payoff at the starting boundary"""
    payoff = old_values[0] + self.omega / (1 - self.beta[1]) * (rhs[0] - (1 - self.beta[1]) * old_values[0] + self.gamma[1] * old_values[1])
    return max(self.payoffs[0], payoff)      
    
  def calculate_payoff_end_boundary(self, rhs, old_values, new_values):
    """Calculate the payoff at the ending boundary"""
    payoff = old_values[-1] + self.omega / (1 - self.beta[-2]) * (rhs[-1] + self.alpha[-2] * new_values[-2] - (1 - self.beta[-2]) * old_values[-1])
    return max(self.payoffs[-1], payoff)
    
  def calculate_payoff(self, k, rhs, old_values, new_values):
    """Calculate the payoff at the k-th point"""
    payoff = old_values[k] + self.omega / (1 - self.beta[k+1]) * (rhs[k] + self.alpha[k + 1] * new_values[k - 1] - (1 - self.beta[k + 1]) * old_values[k] + self.gamma[k + 1] * old_values[k + 1])
    return max(self.payoffs[k], payoff)

  def traverse_grid(self):
    """ Solve using linear systems of equations """
    if self.verbose: print("Traversing the grid")
    aux = np.zeros(self.M - 1)
    new_values = np.zeros(self.M - 1)
    for j in reversed(range(self.N)):
      aux[0] = self.alpha[1] * (self.boundary_values[j] + self.boundary_values[j + 1])
      rhs = np.dot(self.M2, self.past_values) + aux
      old_values = np.copy(self.past_values)
      error = sys.float_info.max
      while self.tol < error:
        new_values[0] = self.calculate_payoff_start_boundary(rhs, old_values)            
        for k in range(self.M-2)[1:]:
          new_values[k] = self.calculate_payoff(k, rhs, old_values, new_values)                    
        new_values[-1] = self.calculate_payoff_end_boundary(rhs, old_values, new_values)
        error = np.linalg.norm(new_values-old_values)
        old_values = np.copy(new_values)
        self.past_values = np.copy(new_values)
    self.values = np.concatenate(
        ([self.boundary_values[0]], new_values, [0]))
    if self.verbose: print("Grid traversed")

  def interpolate(self):
    """ Use piecewise linear interpolation on the initial grid column to get the closest price at S."""
    if self.verbose: print("Interpolating the option price")
    return np.interp(self.S, self.boundary_conds, self.values)

class _BinomialCRRLattice(Option):
  def setup_parameters(self):
    """ Required calculations for the model"""
    if self.verbose: print("Setting up parameters")
    self.u = math.exp(self.sigma * math.sqrt(self.dt))
    self.d = 1 / self.u
    self.qu = (math.exp((self.r - self.div)*self.dt) - self.d) / (self.u-self.d)
    self.qd = 1 - self.qu
    self.M = 2 * self.N + 1
    if self.verbose: print("Parameters set up")

  def init_stock_price_tree(self):
    """ Function for the initialization of the stock price tree"""
    if self.verbose: print("Initializing stock price tree")
    self.STs = np.zeros(self.M)
    self.STs[0] = self.S * self.u ** self.N
    for i in range(self.M)[1:]:
      self.STs[i] = self.STs[i-1]*self.d
    if self.verbose: print("Stock price tree initialized")
  
  def init_payoffs_tree(self):
    """ Function for the initialization of the payoffs tree"""
    if self.verbose: print("Initializing payoffs tree")
    odd_nodes = self.STs[::2]  
    if self.is_call:
        return np.maximum(0, odd_nodes-self.K)
    else:
        return np.maximum(0, self.K-odd_nodes)
    
  def check_early_exercise(self, payoffs):
    """ Function to check for early exercise of the option"""
    self.STs = self.STs[1:-1] 
    odd_STs = self.STs[::2]
    if self.is_call:
        return np.maximum(payoffs, odd_STs-self.K)
    else:
        return np.maximum(payoffs, self.K-odd_STs)
    
  def traverse_tree(self, payoffs):
    """ Function to traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
      payoffs = (payoffs[:-1]*self.qu + 
                 payoffs[1:]*self.qd)*self.df
      if not self.is_european:
          payoffs = self.check_early_exercise(payoffs)
    if self.verbose: print("Tree traversal complete")
    return payoffs
  
  def begin_tree_traversal(self):
    if self.verbose: print("Beginning tree traversal")
    payoffs = self.init_payoffs_tree()
    return self.traverse_tree(payoffs)
  
  def price(self):
    if self.verbose: print("Pricing the option")
    self.setup_parameters()
    self.init_stock_price_tree()
    payoffs = self.begin_tree_traversal()
    if self.verbose: print("Option priced")
    return payoffs[0]

class _TrinomialLattice(Option):
  def setup_parameters(self):
    """ Required calculations for the model """
    if self.verbose: print("Setting up parameters")
    self.u = math.exp(self.sigma * math.sqrt(2 * self.dt))
    self.d = 1/self.u
    self.m = 1
    self.qu = ((math.exp((self.r-self.div) * self.dt/2) - math.exp(-self.sigma * math.sqrt(self.dt / 2))) / (math.exp(self.sigma * math.sqrt(self.dt / 2)) - math.exp(-self.sigma * math.sqrt(self.dt / 2)))) ** 2
    self.qd = ((math.exp(self.sigma * math.sqrt(self.dt/2)) - math.exp((self.r - self.div) * self.dt / 2)) / (math.exp(self.sigma * math.sqrt(self.dt / 2)) - math.exp(-self.sigma * math.sqrt(self.dt / 2)))) ** 2
    self.qm = 1 - self.qu - self.qd
    self.M = 2 * self.N + 1
    if self.verbose: print("Parameters set up")

  def init_stock_price_tree(self):
    """ Initialize the stock price tree """
    if self.verbose: print("Initializing stock price tree")
    self.STs = np.zeros(self.M)
    self.STs[0] = self.S * self.u**self.N
    for i in range(self.M)[1:]:
      self.STs[i] = self.STs[i-1]*self.d
    if self.verbose: print("Stock price tree initialized")

  def init_payoffs_tree(self):
    """ Initialize the payoffs tree """
    if self.verbose: print("Initializing payoffs tree")
    if self.is_call:
      return np.maximum(0, self.STs-self.K)
    else:
      return np.maximum(0, self.K-self.STs)
    
  def check_early_exercise(self, payoffs):
    """ Check for early exercise of the option """
    self.STs = self.STs[1:-1]  
    if self.is_call:
      return np.maximum(payoffs, self.STs-self.K)
    else:
      return np.maximum(payoffs, self.K-self.STs)
  
  def traverse_tree(self, payoffs):
    """ Traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
      payoffs = (payoffs[:-2] * self.qu + payoffs[1:-1] * self.qm + payoffs[2:] * self.qd) * self.df
      if not self.is_european:
          payoffs = self.check_early_exercise(payoffs)
    if self.verbose: print("Tree traversal complete")
    return payoffs
  
  def begin_tree_traversal(self):
    """ Begin the tree traversal """
    if self.verbose: print("Beginning tree traversal")
    payoffs = self.init_payoffs_tree()
    return self.traverse_tree(payoffs)
  
  def price(self):
    """  The pricing implementation """
    if self.verbose: print("Pricing the option")
    self.setup_parameters()
    self.init_stock_price_tree()
    payoffs = self.begin_tree_traversal()
    if self.verbose: print("Option priced")
    return payoffs[0]

class _BinomialTree(Option):
  """Internal class to implement the Binomial Tree Method for option pricing"""
  def setup_parameters(self):
    if self.verbose: print("Setting up parameters")
    self.M = self.N + 1  
    self.u = 1 + self.pu
    self.d = 1 - self.pd_
    self.qu = (math.exp((self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
    self.qd = 1-self.qu
    if self.verbose: print("Parameters set up")

  def init_stock_price_tree(self):
    """ Initialize the stock price tree """
    if self.verbose: print("Initializing stock price tree")
    self.STs = np.zeros(self.M)
    for i in range(self.M):
        self.STs[i] = self.S * (self.u**(self.N-i)) * (self.d**i)
    if self.verbose: print(f"Stock price tree initialized")

  def init_payoffs_tree(self):
    """
    Returns the payoffs when the option 
    expires at terminal nodes
    """
    if self.verbose: print("Initializing payoffs tree") 
    if self.is_call:
      return np.maximum(0, self.STs-self.K)
    else:
        return np.maximum(0, self.K-self.STs)
    
  def traverse_tree(self, payoffs):
    """
    Starting from the time the option expires, traverse
    backwards and calculate discounted payoffs at each node
    """
    if self.verbose: print("Traversing tree")
    for i in range(self.N):
      payoffs = (payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
    if self.verbose: print("Tree traversal complete")
    return payoffs
  
  def begin_tree_traversal(self):
    """Traversal of the tree from the beginning"""
    if self.verbose: print("Beginning tree traversal")
    payoffs = self.init_payoffs_tree()
    return self.traverse_tree(payoffs)
  
  def price(self):
    """ Entry point of the pricing implementation """
    if self.verbose: print("Pricing the option")
    self.setup_parameters()
    self.init_stock_price_tree()
    payoffs = self.begin_tree_traversal()
    if self.verbose: print("Option priced")
    return payoffs[0]

class _USBinomialTree(_BinomialTree):
  def init_stock_price_tree(self):
    """ Initialize the stock price tree"""
    if self.verbose: print("Initializing stock price tree")
    self.STs = [np.array([self.S])]
    for i in range(self.N):
      prev_branches = self.STs[-1]
      st = np.concatenate(
          (prev_branches*self.u, 
           [prev_branches[-1]*self.d]))
      self.STs.append(st)
    if self.verbose: print("Stock price tree initialized")

  def init_payoffs_tree(self):
    """ Initialize the payoffs tree"""
    if self.verbose: print("Initializing payoffs tree")
    if self.is_call:
        return np.maximum(0, self.STs[self.N]-self.K)
    else:
        return np.maximum(0, self.K-self.STs[self.N])

  def check_early_exercise(self, payoffs, node):
    """ Check for early exercise of the option"""
    if self.is_call:
        return np.maximum(payoffs, self.STs[node] - self.K)
    else:
        return np.maximum(payoffs, self.K - self.STs[node])

  def traverse_tree(self, payoffs):
    """ Traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
        payoffs = (payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
        payoffs = self.check_early_exercise(payoffs,i)
    if self.verbose: print("Tree traversal complete")
    return payoffs
  
class _BinomialCRR(_USBinomialTree):
  def setup_parameters(self):
    """ Required calculations for the model """
    if self.verbose: print("Setting up parameters")
    self.u = math.exp(self.sigma * math.sqrt(self.dt))
    self.d = 1./self.u
    self.qu = (math.exp((self.r-self.div)*self.dt) - 
               self.d)/(self.u-self.d)
    self.qd = 1-self.qu
  
  def traverse_tree(self, payoffs):
    """ Traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
        payoffs = (payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
        if not self.is_european:
          payoffs = self.check_early_exercise(payoffs,i)
    if self.verbose: print("Tree traversal complete")
    return payoffs
  
class _BinomialLR(_USBinomialTree):
  def setup_parameters(self):
    """ Required calculations for the model """
    odd_N = self.N if (self.N%2 == 0) else (self.N+1)
    d1 = (math.log(self.S/self.K) +
          ((self.r-self.div) +
           (self.sigma**2)/2.)*self.T)/\
        (self.sigma*math.sqrt(self.T))
    d2 = (math.log(self.S/self.K) +
          ((self.r-self.div) -
           (self.sigma**2)/2.)*self.T)/\
        (self.sigma * math.sqrt(self.T))
    pbar = self.pp_2_inversion(d1, odd_N)
    self.p = self.pp_2_inversion(d2, odd_N)
    self.u = 1/self.df * pbar/self.p
    self.d = (1/self.df-self.p*self.u)/(1-self.p)
    self.qu = self.p
    self.qd = 1-self.p

  def pp_2_inversion(self, z, n):
    """ Peizer-Pratt inversion """
    if self.verbose: print("Calculating Peizer-Pratt inversion")
    return .5 + math.copysign(1, z)*\
        math.sqrt(.25 - .25*
            math.exp(
                -((z/(n+1./3.+.1/(n+1)))**2.)*(n+1./6.)
            )
        )  
  
  def traverse_tree(self, payoffs):
    """ Traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
        payoffs = (payoffs[:-1]*self.qu + payoffs[1:]*self.qd)*self.df
        if not self.is_european:
          payoffs = self.check_early_exercise(payoffs,i)
    if self.verbose: print("Tree traversal complete")
    return payoffs 

class _TrinomialTree(_USBinomialTree):
  def setup_parameters(self):
    """ Required calculations for the model """
    if self.verbose: print("Setting up parameters")
    self.u = math.exp(self.sigma*math.sqrt(2.*self.dt))
    self.d = 1/self.u
    self.m = 1
    self.qu = ((math.exp((self.r-self.div) *
                         self.dt/2.) -
                math.exp(-self.sigma *
                         math.sqrt(self.dt/2.))) /
               (math.exp(self.sigma *
                         math.sqrt(self.dt/2.)) -
                math.exp(-self.sigma *
                         math.sqrt(self.dt/2.))))**2
    self.qd = ((math.exp(self.sigma *
                         math.sqrt(self.dt/2.)) -
                math.exp((self.r-self.div) *
                         self.dt/2.)) /
               (math.exp(self.sigma *
                         math.sqrt(self.dt/2.)) -
                math.exp(-self.sigma *
                         math.sqrt(self.dt/2.))))**2.
    self.qm = 1 - self.qu - self.qd
    if self.verbose: print("Parameters set up")

  def init_stock_price_tree(self):
    """ Initialize the stock price tree """
    if self.verbose: print("Initializing stock price tree")
    self.STs = [np.array([self.S])]
    for i in range(self.N):
      prev_nodes = self.STs[-1]
      self.ST = np.concatenate(
          (prev_nodes*self.u, [prev_nodes[-1]*self.m,
                               prev_nodes[-1]*self.d]))
      self.STs.append(self.ST)
    if self.verbose: print("Stock price tree initialized")

  def traverse_tree(self, payoffs):
    """ Traverse the tree and calculate the option price"""
    if self.verbose: print("Traversing tree")
    for i in reversed(range(self.N)):
      payoffs = (payoffs[:-2] * self.qu +
                 payoffs[1:-1] * self.qm +
                 payoffs[2:] * self.qd) * self.df
      if not self.is_european:
        payoffs = self.check_early_exercise(payoffs,i)
    if self.verbose: print("Tree traversal complete")
    return payoffs

class _BlackScholes(Option):
  def price(self):
    """ Calculate the option price using the Black-Scholes formula """
    if self.verbose: print("Calculating the option price using the Black-Scholes formula")
    d1 = (math.log(self.S/self.K) + ((self.r-self.div) + (self.sigma**2)/2.)*self.T) / (self.sigma*math.sqrt(self.T))
    d2 = d1 - self.sigma * math.sqrt(self.T)
    if self.is_call:
      return self.S * math.exp(-self.div*self.T) * norm.cdf(d1) - self.K * math.exp(-self.r*self.T) * norm.cdf(d2)
    else:
      return self.K * math.exp(-self.r*self.T) * norm.cdf(-d2) - self.S * math.exp(-self.div*self.T) * norm.cdf(-d1)

class _MonteCarlo(Option):
  """Internal class to implement the Monte Carlo Method for option pricing"""
  def __init__(self, S, K, r, T, N, pu, pd_, div, sigma, num_of_paths, call=True, american=False, verbose = False, display = False):
    """
    Inputs:
    - S: float, the price of the underlying asset
    - K: float, the strike price of the option
    - r: float, the risk-free rate
    - T: float, the time to expiration of the option
    - N: int, the number of time steps
    - pu: float, the probability of an up movement
    - pd_: float, the probability of a down movement
    - div: float, the dividend yield
    - sigma: float, the volatility of the underlying asset
    - num_of_paths: int, the number of paths to simulate
    - call: bool, whether the option is a call or a put
    - american: bool, whether the option is American or European
    - verbose: bool, the verbosity of the output
    - display: bool, whether to display the asset price paths
    """
    super().__init__(S, K, r, T, N, pu, pd_, div, sigma, call, american, verbose)
    self.num_of_paths = num_of_paths
    self.verbose = verbose
    self.show = display
  
  def simulate_price(self):
    """ Function to simulate the price of the underlying asset"""
    if self.verbose: print("Simulating the price of the underlying asset")
    S = np.zeros((self.N + 1, self.num_of_paths))
    S[0] = self.S
    for t in range(1, self.N+1):
      drift = (self.r - self.div - 0.5 * self.sigma ** 2) * self.dt
      Z = np.random.randn(self.num_of_paths)
      diffusion = self.sigma * np.sqrt(self.dt) * Z
      S[t] = S[t-1] * np.exp(drift + diffusion)
    self.STs = S
    if self.verbose: print("Price simulation complete")
  
  def display(self):
    plt.figure(figsize=(10,10))
    sns.lineplot(data = self.STs)
    plt.title("Simulated Asset Price Paths")
    plt.xlabel("Time Steps")
    plt.ylabel("Asset Price")
    plt.gca().get_legend().remove()
    plt.show()

  def price(self):
    if self.verbose: print("Calculating the option prices using the Monte Carlo method")
    self.simulate_price()
    if self.is_european:
      if self.is_call:
        payoffs = np.maximum(self.STs[-1] - self.K, 0)
      else:
        payoffs = np.maximum(self.K - self.STs[-1], 0)
      option_prices = np.exp(-(self.r - self.div) * self.T) * payoffs
      print("Averaging the option prices")
      if self.verbose: print("Calculating the average option price")
      if self.show:
        self.display()
      return np.mean(option_prices)
    else:
      if self.is_call:
        payoffs = np.maximum(self.STs - self.K, 0)
      else:
        payoffs = np.maximum(self.K - self.STs, 0)
      for t in reversed(range(self.N)):
        in_the_money = np.where(payoffs[t] > 0)[0]
        if len(in_the_money) > 0:
          regression = np.polyfit(self.STs[t, in_the_money], payoffs[t, in_the_money] * self.df, 2)
          continuation_value = np.polyval(regression, self.STs[t, in_the_money])
          if self.is_call:
            exercise_values = np.maximum(self.STs[t, in_the_money] - self.K, 0)
          else:
            exercise_values = np.maximum(self.K - self.STs[t, in_the_money], 0)
          exercise = exercise_values > continuation_value
          payoffs[t, in_the_money[exercise]] = exercise_values[exercise]
          payoffs *= self.df
      if self.verbose: print("Calculating the average option price")
      if self.show:
        self.display()
      return np.mean(payoffs[0])   

class _FDUS(_FDEU):
  """Internal class to implement the Explicit Finite Difference Method for American options"""

  def traverse_grid(self):
    if self.verbose: print("Traversing the grid for U.S. option")
    for j in reversed(range(self.N)): 
      for i in range(1, self.M): 
          calculated_value = self.a[i] * self.grid[i-1, j+1] + self.b[i] * self.grid[i, j+1] + self.c[i] * self.grid[i+1, j+1]
          intrinsic_value = max(self.boundary_conds[i] - self.K, 0) if self.is_call else max(self.K - self.boundary_conds[i], 0)
          self.grid[i, j] = max(calculated_value, intrinsic_value)
    if self.verbose: print("Grid traversed with early exercise considered")

class _FDImpUS(_FDImpEU):
  def traverse_grid(self):
    """ Solve using linear systems of equations """
    if self.verbose: print("Traversing the grid for U.S. option")
    P, L, U = linalg.lu(self.coeffs)
    aux = np.zeros(self.M-1)
    for i in reversed(range(self.N)):
      aux[0] = np.dot(-self.a[1], self.grid[0, i])
      x1 = linalg.solve(L, self.grid[1:self.M, i+1]+aux)
      x2 = linalg.solve(U, x1)
      self.grid[1:self.M, i] = x2
      intrinsic_values = np.maximum(self.boundary_conds[1:self.M] - self.K, 0) if self.is_call else np.maximum(self.K - self.boundary_conds[1:self.M], 0)
      self.grid[1:self.M, i] = np.maximum(self.grid[1:self.M, i], intrinsic_values)
    if self.verbose: print("Grid traversed with early exercise considered")

class OptionPricing(object):
  def __init__(self, 
               ticker: str,
               call: bool,
               american: bool,
               risk_free_rate: Union[str, float],
               identification: Union[str, int],
               risk_free_rate_approximation: str = 'last_observed',
               volatility: float = None,
               use_yfinance_volatility: bool = True,
               optimize_garch: bool = False,
               optimization_rounds: int = 100,
               verbose: bool = False,
               risk_free_rate_approximation_parameters: dict = {},
               num_of_days_risk_free_rate: int = 252,
               num_of_days_volatility: int = 252,
               ):
    """
    Class to price options using different methods.
    Inputs:
    - ticker: str, can be either the name of the company or the ticker
    - call: bool, whether the option is a call or a put
    - american: bool, whether the option is American or European
    - risk_free_rate: either a string representing the horizon or a value
    - identification: either a string representing the contract symbol or an integer representing the index of the option within the chain
    - risk_free_rate_approximation: str, the method to approximate the risk-free rate, can be 'last_observed', 'SMA', 'EMA', 'SARIMAX'
    - volatility: float, the volatility of the underlying asset
    - use_yfinance_volatility: bool, whether to use the volatility from Yahoo Finance if no volatility is provided. If False, a GARCH model will be used
    - optimize_garch: bool, whether to optimize the GARCH model for the volatility
    - optimization_rounds: int, the number of rounds to optimize the GARCH model
    - verbose: bool, whether to print the steps of the process
    - risk_free_rate_approximation_parameters: dict, the parameters to be passed to the risk-free rate approximation method
    - num_of_days_risk_free_rate: int, the number of days to consider for the risk-free rate approximation
    - num_of_days_volatility: int, the number of days to consider for the volatility approximation
    """
    if type(ticker) != str:
      raise ValueError('ticker must be a string')
    if type(call) != bool:
      raise ValueError('call must be a boolean')
    if type(american) != bool:
      raise ValueError('american must be a boolean')
    if (type(volatility) != float) and (volatility is not None) and (type(volatility) != int):
      raise ValueError('volatility must be a number')
    if type(use_yfinance_volatility) != bool:
      raise ValueError('use_yfinance_volatility must be a boolean')
    if type(optimize_garch) != bool:
      raise ValueError('optimize_garch must be a boolean')
    if type(optimization_rounds) != int:
      raise ValueError('optimization_rounds must be an integer')
    if type(verbose) != bool:
      raise ValueError('verbose must be a boolean')
    self.fetcher = Fetcher(ticker)
    self.dataframe, self.yf_ticker = self.fetcher.df, self.fetcher.yf_stock
    if type(identification) == str:
      self.option_chain = self.yf_ticker.option_chain().calls if call else self.yf_ticker.option_chain().puts
      self.option = self.option_chain[self.option_chain['contractSymbol'] == identification]
    elif type(identification) == int:
      self.option = self.yf_ticker.option_chain().calls.iloc[identification] if call else self.yf_ticker.option_chain().puts.iloc[identification]
    else:
      raise ValueError('identification must be either a string or an integer')
    self.verbose = verbose
    self.date = self._calculate_expiration()
    self.is_call = call
    self.dividend_yield = self.fetcher.get_dividend_yield()
    if type(risk_free_rate) == str:
      self.historical = self.fetcher.get_risk_free_rate(risk_free_rate)['Close'].tail(num_of_days_risk_free_rate)
      if risk_free_rate_approximation == 'last_observed':
        self.risk_free_rate = self.historical.iloc[-1]
      elif risk_free_rate_approximation == 'SMA':
        if 'window' not in risk_free_rate_approximation_parameters.keys():
          print("Window not passed, using default value of 20")
        if 'num_of_steps' not in risk_free_rate_approximation_parameters.keys():
          print("Number of steps not passed, using default value of 1")
        window = risk_free_rate_approximation_parameters.get('window', 20)
        num_of_steps = risk_free_rate_approximation_parameters.get('num_of_steps', 1)
        SMA = _SMA(self.historical, window)
        self.risk_free_rate = SMA.predict_val(num_of_steps)
      elif risk_free_rate_approximation == 'EMA':
        if 'window' not in risk_free_rate_approximation_parameters.keys():
          print("Window not passed, using default value of 20")
        if 'num_of_steps' not in risk_free_rate_approximation_parameters.keys():
          print("Number of steps not passed, using default value of 1")
        window = risk_free_rate_approximation_parameters.get('window', 20)
        num_of_steps = risk_free_rate_approximation_parameters.get('num_of_steps', 1)
        self.risk_free_rate = _EMA(self.historical, window).predict_val(num_of_steps)
      elif risk_free_rate_approximation == 'SARIMAX':
        if verbose:
          print("The SARIMAX method accepts the following optional parameters:\n - exog: pd.Series, exogenous variable to use in the model")
          print("- forecast_steps: int, number of forecast steps")
          print("- optimize: bool, whether to optimize the hyperparameters")
          print("- optimization_rounds: int, number of rounds to optimize the hyperparameters")
          print("- test_size: float, size of the test set")
          print("- random_state: int, random state for reproducibility")
          print("- p: int, AR order")
          print("- d: int, differencing order")
          print("- q: int, MA order")
          print("- P: int, seasonal AR order")
          print("- D: int, seasonal differencing order")
          print("- Q: int, seasonal MA order")
          print("- s: int, seasonal period")
          print("- trend: str, trend parameter")
          print("- measure_error: bool, whether to measure the error")
          print("- time_varying_regression: bool, whether to use time varying regression")
          print("- mle_regression: bool, whether to use MLE regression")
          print("- simple_differencing: bool, whether to use simple differencing")
          print("- enforce_stationarity: bool, whether to enforce stationarity")
          print("- enforce_invertibility: bool, whether to enforce invertibility")
          print("- hamilton_representation: bool, whether to use Hamilton representation")
          print("- concentrate_scale: bool, whether to concentrate scale")
          print("- trend_offset: int, trend offset")
          print("- use_exact_diffuse: bool, whether to use exact diffuse")
        if 'forecast_steps' in risk_free_rate_approximation_parameters.keys():
          steps = risk_free_rate_approximation_parameters['forecast_steps']
          risk_free_rate_approximation_parameters.pop('forecast_steps')
        if steps is None or not isinstance(steps, int):
          steps = 1
        model = _SARIMAX_model(self.historical, **risk_free_rate_approximation_parameters)
        self.risk_free_rate = np.mean(model.forecast(steps))

    elif type(risk_free_rate) == float or type(risk_free_rate) == int:
      self.risk_free_rate = risk_free_rate
    else:
      raise ValueError('risk_free_rate must be either a string representing the horizon or a value')
    self.r = self.risk_free_rate * 100
    self.S = self.dataframe['Close'].iloc[-1]
    self.T = (self.date - pd.to_datetime('today')).days / 365
    self.K = self.option['strike']
    self.american = american
    self.num_of_days_volatility = num_of_days_volatility
    if use_yfinance_volatility:
      self.sigma = self.option['impliedVolatility']
    else:
      if optimize_garch:
        garch_params = self.optimize_garch_model(optimization_rounds)
        self.build_garch_model(**garch_params)
      else:
        self.build_garch_model('GARCH', 'Constant', 1, 1, 'normal', 0, 2, None, None) 
      res = self.garch_model.fit(disp='off')
      sigma = res.conditional_volatility
      self.sigma = sigma[-1]
    if volatility is not None:
      self.sigma = volatility

  def _from_name_to_datestr(self, s: str) -> str:
    """Helper function to convert the contract symbol to a date string"""
    if self.verbose:
      print(f"Processing {s}")
    match = re.search(r'[A-Za-z](\d{2})(\d{2})(\d{2})[CP]', s)
    if match:
        year, month, day = match.groups()
        return f"20{year}-{month}-{day}"
    else:
        return "No date found"
  
  def _calculate_expiration(self) -> pd.Timestamp:
    """Function to calculate the expiration date of the option"""
    if self.verbose:
      print("Calculating expiration date")
    to_process = self.option['contractSymbol']
    date_str = self._from_name_to_datestr(to_process)
    date = pd.to_datetime(date_str)
    return date 
  
  def calculate_option_price(self, method: str, describe: bool = False, **kwargs) -> float:
    """
    Main wrapper function to calculate the price of an option using the specified method.
    Inputs:
      - method: str, the method to use for pricing
      - describe: bool, whether to describe the method
      - kwargs: additional arguments to be passed to the method
    
    Accepted methods:
    - Binomial Tree Methods: Binomial Tree, Binomial Lattice Tree, Cox-Ross-Rubinstein, Leisen-Reimer Tree
    - Trinomial Tree Methods: Trinomial Tree, Trinomial Lattice Tree
    - Finite Difference Methods: Explicit Finite Difference, Implicit Finite Difference, Crank-Nicolson Finite Difference
    """
    method = method.replace(' ', '').lower()
    if method in ('blackscholes', 'black-scholes', 'bs', 'black_scholes'):
      if self.american:
        raise MethodError("The Black-Scholes method is only available for European options")
      if describe:
        print("The Black-Scholes Method requires no additional values")
      price = self.black_scholes()
      return price
    
    if method in ('montecarlo', 'monte-carlo', 'mc', 'monte_carlo'):
      if 'num_of_paths' not in kwargs:
        print("num_of_paths not passed, using default value of 1000")
      if 'N' not in kwargs:
        print("N not passed, using default value of 1000")
      if 'display' not in kwargs:
        print("display not passed, using default value of False")
      if describe:
        print("The Monte Carlo Method requires three optional value,")
        print("num_of_paths, which is the number of paths to simulate")
        print("N, which is the number of time steps")
        print("display, which is whether to display the asset price paths")
      num_of_paths = kwargs.get('num_of_paths', 1000)
      N = kwargs.get('N', 1000)
      display = kwargs.get('display', False)
      if type(N) != int:
        raise ValueError("N must be an integer")
      if type(num_of_paths) != int:
        raise ValueError("num_of_paths must be an integer")
      if type(display) != bool:
        raise ValueError("display must be a boolean")
      price = self.montecarlo(num_of_paths, N, display)
      return price

    if method in ('binomialtree', 'binomial', 'binomtree', 'binom'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 1000")
      if 'pd_' not in kwargs:
        print("pd_ not passed, using default value of 0.01")
      if 'pu' not in kwargs:
        print("pu not passed, using default value of 0.01")
      if describe:
        print("The Binomial Tree Method requires three optional values,")
        print("N, which is the number of time steps")
        print("pd_, which is the probability at the down state")
        print("pu, which is the probability at the up state")
      N = kwargs.get('N', 1000)
      pd_ = kwargs.get('pd_', 1e-2)
      pu = kwargs.get('pu', 1e-2)
      if self.american:
        price = self.binom_american(N, pd_, pu)
      else:
        price = self.binom_european(N, pd_, pu)
      return price
    
    if method in ('binomiallattice', 'binomial_lattice', 'binomlattice', 'binom_lattice'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 2")
      if describe:
        print("The Binomial Lattice Method requires one optional values,")
        print("N, which is the number of time steps")
      N = kwargs.get('N', 2)
      price = self.binom_lattice(N)
      return price
    
    if method in ('cox-ross-rubinstein', 'cox', 'coxrossrubinstein', 'crr'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 10")
      if describe:
        print("The Cox-Ross-Rubinstein Method requires one optional values,")
        print("N, which is the number of time steps")
      N = kwargs.get('N', 10)
      price = self.cox_ross_rubinstein(N)
      return price
    
    if method in ('leisen-reimertree', 'lrtree', 'lr'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 5")
      if describe:
        print("The Leisen-Reimer Tree Method requires one optional value,")
        print("N, which is the number of time steps")
      N = kwargs.get('N', 5)
      price = self.lr_tree(N)
      return price
    
    if method in ('trinomialtree', 'trinomial', 'trinom'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 1000")
      N = kwargs.get('N', 1000)
      if describe:
        print("The Trinomial Tree Method requires one optional value,")
        print("N, which is the number of time steps")
      price = self.trinom(N)
      return price
    
    if method in ('trinomiallattice', 'trinomial_lattice', 'trinomlattice', 'trinom_lattice'): #Check
      if 'N' not in kwargs:
        print("N not passed, using default value of 2")
      N = kwargs.get('N', 2)
      if describe:
        print("The Trinomial Lattice Method requires three optional values,")
        print("N, which is the number of time steps")
      price = self.trinom_lattice(N)
      return price
    
    if method in ('finitedifference', 'finite_difference'):
      raise MethodError("Please specify between Explicit Finite Difference, Implicit Finite Difference and Crank-Nicolson Finite Difference")
    
    if method in ('explicitfinitedifference', 'explicit', 'explicitdifference', 'explicitfinite', 'explicit_difference'):
      if 'Smax' not in kwargs:
        print("Smax not passed, using default value of 1000")
      if 'M' not in kwargs:
        print("M not passed, using default value of 50")
      if 'N' not in kwargs:
        print("N not passed, using default value of 50")
      Smax = kwargs.get('Smax', 1000)
      M = kwargs.get('M', 50)
      N = kwargs.get('N', 50)
      if describe:
        print("The Explicit Finite Difference Method requires three optional values,")
        print("Smax, which is the maximum value of the underlying asset")
        print("M, which is the number of price steps")
        print("N, which is the number of time steps")
      if self.american:
        price = self.explicit_american(Smax, M, N)
      else:
        price = self.explicit_european(Smax, M, N)
      return price
    
    if method in ('implicitfinitedifference', 'implicit', 'implicitdifference', 'implicitfinite'):
      if 'Smax' not in kwargs:
        print("Smax not passed, using default value of 1000")
      if 'M' not in kwargs:
        print("M not passed, using default value of 1000")
      if 'N' not in kwargs:
        print("N not passed, using default value of 1000")
      Smax = kwargs.get('Smax', 1000)
      M = kwargs.get('M', 1000)
      N = kwargs.get('N', 1000)
      if describe:
        print("The Implicit Finite Difference Method requires three optional values,")
        print("Smax, which is the maximum value of the underlying asset")
        print("M, which is the number of price steps")
        print("N, which is the number of time steps")
      if self.american:
        price = self.implicit_american(Smax, M, N)
      else:
        price = self.implicit_european(Smax, M, N)
      return price
    
    if method in ('crank-nicolsonfinitedifference', 'crank-nicolson', 'cranknicolson', 'crank-nicolsonfinite', 'crank-nicolsondifference', 'cranknicolsonfinite', 'cranknicolsondifference', 'crank_nicolson', 'crank_nicolson_finite', 'crank_nicolson_difference','crank_nicolson_finite_difference', 'cnfd', 'cn'):
      if self.american:
        if 'Smax' not in kwargs:
          print("Smax not passed, using default value of 1000")
        if 'M' not in kwargs:
          print("M not passed, using default value of 100")
        if 'N' not in kwargs:
          print("N not passed, using default value of 100")
        if 'omega' not in kwargs:
          print("omega not passed, using default value of 1.2")
        if 'tol' not in kwargs:
          print("tol not passed, using default value of 1e-2")
        Smax = kwargs.get('Smax', 1000)
        M = kwargs.get('M', 100)
        N = kwargs.get('N', 100)
        omega = kwargs.get('omega', 1.2)
        tol = kwargs.get('tol', 1e-2)
        if describe:
          print("The Crank-Nicolson Finite Difference Method for american options requires five optional values,")
          print("Smax, which is the maximum value of the underlying asset")
          print("M, which is the number of price steps")
          print("N, which is the number of time steps")
          print("omega, which is the relaxation factor")
          print("tol, which is the tolerance")
        price = self.crank_nicolson_american(Smax, M, N, omega, tol)
      else:
        if 'Smax' not in kwargs:
          print("Smax not passed, using default value of 1000")
        if 'M' not in kwargs:
          print("M not passed, using default value of 100")
        if 'N' not in kwargs:
          print("N not passed, using default value of 100")
        Smax = kwargs.get('Smax', 1000)
        M = kwargs.get('M', 100)
        N = kwargs.get('N', 100)
        if describe:
          print("The Crank-Nicolson Finite Difference Method for european options requires three optional values,")
          print("Smax, which is the maximum value of the underlying asset")
          print("M, which is the number of price steps")
          print("N, which is the number of time steps")
        price = self.crank_nicolson_european(Smax, M, N)
      return price
    raise MethodError(f"Method {method} not found")
  
  def montecarlo(self, num_of_paths: int = 1000, N: int = 1000, display = False, pu = 0, pd_ = 0) -> float:
    mc = _MonteCarlo(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, num_of_paths, self.is_call, self.american, self.verbose, display)
    return mc.price()

  def black_scholes(self, N = 100, pu = 0, pd_ = 0) -> float:
    bs = _BlackScholes(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return bs.price()

  def crank_nicolson_american(self, Smax: int = 1000, M: int = 100, N: int = 100, omega: float = 1.2, tol: float = 1e-3) -> float:
    us = _FDCNUS(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, omega, tol, self.is_call, self.verbose)
    return us.price()

  def crank_nicolson_european(self, Smax: int = 1000, M: int = 100, N: int = 100) -> float:
    eu = _FDCN(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, self.is_call, self.verbose)
    return eu.price()

  def implicit_american(self, Smax: int = 1000, M: int = 1000, N: int = 1000) -> float:
    us = _FDImpUS(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, self.is_call, self.verbose)
    return us.price()

  def implicit_european(self, Smax: int = 1000, M: int = 1000, N: int = 1000) -> float: 
    eu = _FDImpEU(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, self.is_call, self.verbose)
    return eu.price() 

  def explicit_american(self, Smax: int = 1000, M: int = 1000, N: int = 1000) -> float:
    us = _FDUS(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, self.is_call, self.verbose)
    return us.price()

  def explicit_european(self, Smax: int = 1000, M: int = 1000, N: int = 1000) -> float:
    eu = _FDEU(self.S, self.K, self.r, self.T, self.sigma, Smax, M, N, self.is_call, self.verbose)
    return eu.price() 

  def trinom_lattice(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    option = _TrinomialLattice(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return option.price()

  def binom_lattice(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    option = _BinomialCRRLattice(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return option.price()

  def trinom(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    option = _TrinomialTree(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return option.price()
  
  def lr_tree(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    opt = _BinomialLR(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return opt.price()

  def cox_ross_rubinstein(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    opt = _BinomialCRR(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return opt.price()

  def binom_american(self, N: int = 1000, pd_: float = 0, pu: float = 0) -> float:
    us = _USBinomialTree(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return us.price()
  
  def binom_european(self, N: int, pd_: float, pu: float) -> float:
    eu = _BinomialTree(self.S, self.K, self.risk_free_rate, self.T, N, pu, pd_, self.dividend_yield, self.sigma, self.is_call, self.american, self.verbose)
    return eu.price()
  
  def build_garch_model(self, vol, mean, p, q, dist, o, power, hold_back, rescale):
    if self.verbose: print("Building GARCH model")
    target_val = self.dataframe['Close'].pct_change().dropna() * 100
    target_val = target_val.tail(self.num_of_days_volatility)
    self.garch_model = arch.arch_model(target_val, vol = vol, mean = mean, p=p, q=q, dist=dist, o=o, power=power, hold_back=hold_back, rescale=rescale)
    if self.verbose: print("GARCH model built")

  def optimize_garch_model(self, optimization_trials) -> dict:
    """
    This function is designed to optimize the GARCH model on the returns of the stock.
    Optuna is used to optimize the parameters of the GARCH model.
    Inputs:
      - optimization_trials: int, the number of trials to run
    Warning: This function is experimental
    """
    if self.verbose: print("Optimizing GARCH model")
    def objective(trial):
        vol =  trial.suggest_categorical('vol', ['GARCH', 'ARCH', 'EGARCH', 'FIGARCH', 'APARCH', 'HARCH'])
        p = trial.suggest_int('p', 0, 10)
        q = trial.suggest_int('q', 0, 10)
        mean = trial.suggest_categorical('mean', ['Constant', 'Zero', 'LS', 'AR', 'ARX', 'HAR', 'HARX', 'constant', 'zero'])
        dist = trial.suggest_categorical('dist', ['normal', 'gaussian', 't', 'studentst', 'skewstudent', 'skewt', 'ged', 'generalized error'])
        o = trial.suggest_int('o', 0, 10)
        power = trial.suggest_float('power', 0, 10)
        hold_back = trial.suggest_int('hold_back', 0, 10)
        if hold_back == 0: hold_back = None
        rescale = trial.suggest_categorical('rescale', [True, False, None])
        if self.verbose: print(f"Optimizing with parameters {vol}, {mean}, {p}, {q}, {dist}, {o}, {power}, {hold_back}, {rescale}")
        try:
            self.build_garch_model(vol, mean, p, q, dist, o, power, hold_back, rescale)
            res = self.garch_model.fit(disp='off')
            return res.aic
        except Exception as e:
            print(f"Error with parameters {p}, {q}, {vol}, {mean}, {dist}, {o}, {power}, {hold_back}, {rescale}: {e}")
            return float('inf')
    print("Warning: This function is experimental, and may throw errors in the optimization process. Use at your own risk.")
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=optimization_trials)
    if self.verbose: print("Optimization complete")
    return study.best_params
  
  def __repr__(self) -> str:
    return f"Option of {self.yf_ticker.ticker}\nStrike Price: {self.K}\nRisk-Free Rate: {self.risk_free_rate}\nExpiration Date: {self.date}\nDividend Yield: {self.dividend_yield}\nPrice of the stock: {self.S}\nVolatility: {self.sigma}\nIs Call: {self.is_call}\nIs an american option: {self.american}\n"
