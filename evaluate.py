def plot_residuals(actual, predicted):
    residuals = actual - predicted
    plt.hlines(0, actual.min(), actual.max(), ls=':')
    plt.scatter(actual, residuals)
    plt.ylabel('residual ($y - \hat{y}$)')
    plt.xlabel('actual value ($y$)')
    plt.title('Actual vs Residual')
    plt.show()

def residuals(actual, predicted):
    return actual - predicted

def SSE(actual, predicted):
    return (residuals(actual, predicted) **2).sum()

def MSE(actual, predicted):
    n = actual.shape[0]
    return SSE(actual, predicted) / n

def RMSE(actual, predicted):
    return math.sqrt(MSE(actual, predicted))

def ESS(actual, predicted):
    return ((predicted - actual.mean()) ** 2).sum()

def TSS(actual):
    return ((actual - actual.mean()) ** 2).sum()

def R2_score(actual, predicted):
    return ess(actual, predicted) / TSS(actual)

def regression_errors(actual, predicted):
    return pd.Series({
        'SSE': SSE(actual, predicted),
        'ess': ess(actual, predicted),
        'TSS': TSS(actual),
        'MSE': MSE(actual, predicted),
        'RMSE': RMSE(actual, predicted),
    })

def baseline_mean_errors(actual):
    predicted = actual.mean()
    return {
        'SSE': SSE(actual, predicted),
        'MSE': MSE(actual, predicted),
        'RMSE': RMSE(actual, predicted),
    }

def better_than_baseline(actual, predicted):
    RMSE_baseline = RMSE(actual, actual.mean())
    RMSE_model = RMSE(actual, predicted)
    return RMSE_model < RMSE_baseline