**Machine Learning Option Pricing:**  
An empirical approach based on market data

# Table of Contents
1. [Introduction](#introduction)
2. [Pricing Model Specification](#pricing-model-specification)
   - 2.1 [Pricing Model](#pricing-model)
   - 2.2 [Volatility Estimation](#volatility-estimation)
3. [Machine Learning Model Specification](#machine-leanring-model-specification)
   - 3.1 [Scope](#scope)
5. [References](#references)


# 1. Introduction

The main scope of this paper is to devise a data generation method that can be reliably used to train machine learning algorithms in pricing options under stochastic volatility. It has been demonstrated by Frey et al. (2022) that Single Layer and Deep Neural networks are able to accurately predict vanilla option prices given a large synthetic training dataset. 

The data generation method proposed is an extension of that in Frey et al. (2022) with additional considerations regarding the feasibility of all feature combinations. The machine learning model specification is nearly identical to that of Frey et al. (2022) with minor exceptions including the use of relative absolute pricing error against relative moneyness as a performance metric, as well as exploration of additional parameterisation.

Following this eniqury into the felixbility of this method, it was considered whether ScikitLearn Neural Network models could be used to price path-dependent exotic options. Thus, we aim to generalize a data generation routine utilising generic at-the-money volatilites which will allow us to train the model on data strictly adhering to desired market conditions while allowing for accurately calibrated stochastic volatility for each trading day simulated in part.


# 2. Pricing Model Specification
## 2.1 Pricing Model

To model the logarithmic price of our underlying security, we use the Heston (1993) model, described by the pair of stochastic differential equations:

$$
dX_t = \left( r - \frac{v_t}{2} \right) dt + \sqrt{v_t} \left( \rho dW_t + \sqrt{1 - \rho^2} dB_t \right) \quad (1)
$$

$$
\hspace{1.9cm}  dv_t = \kappa (\theta - v_t) dt + \eta \sqrt{v_t} dW_t \hspace{1.8cm} \quad (1.1)
$$


where
- $v_0$ represents the initial variance,
- $\theta$ is the long-run variance,
- $\rho$ is the correlation between the log-price process and its volatility,
- $\kappa$ is the mean reversion of the variance to **𝜃**,
- $\eta$ is the volatility of the variance process, and 
- $B_t$ , $W_t$ are continuous random walks. 

## 2.2 Volatility Estimation
The model becomes suitable for fitting to our proposed method via approximation of implied volatilities as devised by Derman (2008):

$$
\hspace{1cm} \sigma(K, t_0) = \sigma_{\text{atm}}(S_0, t_0) - b(t_0)(K - S_0) \hspace{1cm} \quad (2)
$$

<br>


# 3. Neural Network Specification
## 3.1 Scope
The scope of our proposed historical simulation method is to test whether machine learning estimations of pricing functions can reliably price large volumes of exotic options in as close of a realistic trading scenario as our methods permit. The main considerations will be around frequency of retraining and choice of model features. In all cases, the model will have the minimum of four features: underlying spot price, strike price, days to maturity, and a categorical 'put'/'call' flag classified with one hot encoding. Further, the model will include the additionals features of barrier level and barrier type and potentially Heston pricing parameters. Following this the model will be extended to Asian arithmetic and geometric options with similar considerations.
 <br>
 <br>
Another major consideration will be that of data management and training data selection. With vast amounts of data available by virtue of the generation method, it is possible that finding the correct selection criteria may depend on multiple factors, lowering the model's flexibility. For pricing performance, the Root Square Mean Error and Mean Absolute Error metrics will be used.

# 4. References
Blanda, V. (2023). FX Barrier Option Pricing. Available at: https://www.imperial.ac.uk/media/imperial-college/faculty-of-natural-sciences/department-of-mathematics/math-finance/212252650---VALENTIN-BLANDA---BLANDA_VALENTIN_02293988.pdf

Derman, E. (2008). Lecture 9: Patterns of Volatility Change. Available at: https://emanuelderman.com/wp-content/uploads/2013/09/smile-lecture9.pdf 

Frey, C., Scheuch, C., Voigt, S. and Weiss, P. (2022). Option Pricing via Machine Learning with Python. Tidy Finance. 
Available at: https://www.tidy-finance.org/python/option-pricing-via-machine-learning.html

Heston, S. (1993). A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options.
Available at: https://www.ma.imperial.ac.uk/~ajacquie/IC_Num_Methods/IC_Num_Methods_Docs/Literature/Heston.pdf
