import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from scipy import stats
from .ultils import seasonal_decompose


def Multivariate_Density(data, features=None, n_features=5):    
    """
    Tạo Pair plot với Multivariate Density plot cho một vài biến bất kỳ

    Parameters:
        data: pandas DataFrame. Input là dataset cần để tạo Pair plot
        features: str, tuỳ chọn. Danh sách các feature hay các biến muốn tạo Pair plot, nếu chọn None, các feature sẽ được chọn ngẫu nhiên
        n_features: int, optional. Số lượng các feature ngẫu nhiên, nếu chọn None, số lượng mặc định là 10

    Returns:
        Vẽ sơ đồ pairplot
    """

    # Nếu không xác định feature thì sẽ chọn ngẫu nhiên
    if features is None:
        features = np.random.choice(data.columns, size=min(len(data.columns),n_features), replace=False).tolist()
    # Chọn những feature đã được lấy thành một DataFrame
    selected_data = data[features]
    # Tạo Pair plot với các feature được chọn
    sns.pairplot(selected_data, diag_kind='kde', kind='reg', plot_kws={'line_kws':{'color':'red'}})

    plt.suptitle('Multivariate Density Plots', y=1.02)
    plt.show()


def Isolation_Forest(data, contamination=0.003, random_state=42, figure_size=(10, 8)):
    
    """
    Sử dụng Isolation Forest để tìm các outliers trong data

    Parameters:
        data: pandas Series hoặc mảng, hình dạng (n_samples). Dữ liệu chuỗi thời gian.
        contamination: float, tùy chọn (mặc định=0.003). Tỷ lệ của các giá trị outliers trong tập dữ liệu.
        random_state: int hoặc RandomState, tùy chọn (mặc định=42). Điều khiển seed ngẫu nhiên để có thể tái tạo kết quả.
        figure_size: tuple, tùy chọn (mặc định=(10, 8)).Kích thước của hình.

    Return:
        Sơ đồ biểu diễn các outlier trong hình.
    """

    # Khởi tạo mô hình IsolationForest
    clf = IsolationForest(contamination=contamination, random_state=random_state)
    # Huấn luyện mô hình và dự đoán các giá trị ngoại lai
    outliers = clf.fit_predict(data)
    # Trích xuất các giá trị ngoại lai từ dữ liệu đã được scale
    outliers_data = data[outliers == -1]
    outlier_indices = np.where(outliers == -1)[0]

    # Tạo đối tượng hình và trục
    fig, ax = plt.subplots(figsize=figure_size)

    # Vẽ dữ liệu gốc
    ax.plot(data.index, data, c='blue', label='Time Series Data')
    ax.scatter(data.index[outlier_indices], outliers_data, c='red', label='Outlier')
    ax.set_title('Isolation Forest Outlier Detection')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()

    return fig, ax


def IQR(data, threshold=1.5, figure_size=(10, 8)):
    
    """
    Sử dụng IQR để tìm các outliers trong data.

    Parameters:
        data: pandas Series, shape (n_samples). Input là giá close hoặc return.
        threshold: float, tùy chọn (mặc định = 1.5). Ngưỡng để quyết định xem giá trị đó có phải là outlier hay không. Các giá trị ngoài ngưỡng (Q1 - threshold * IQR, Q3 + threshold * IQR) được coi là outlier.
        figure_size: tuple, tùy chọn (mặc định = (10, 8)). Kích thước của hình.

    Returns:
        Sơ đồ biểu diễn các outlier trong hình.

    """

    # Tính khoảng quantile 1 và 3
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    # Tính khoảng IQR
    iqr = q3 - q1

    # Tính khoảng dưới và khoảng trên để phát hiện outlier
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    # Tìm các outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]

    # Vẽ sơ đồ gốc cùng với các outlier đã được tìm thấy
    fig, ax = plt.subplots(figsize=figure_size)

    ax.plot(data.index, data, c='blue', label='Normal')
    ax.scatter(outliers.index, outliers, c='red', label='Outliers')
    ax.set_title('IQR Outlier Detection')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.legend()

    return fig, ax


def MAD(data, threshold=3.5, figsize=(10, 8)):
    
    """
    Sử dụng MAD (Median Absolute Deviation) để tìm các outliers trong data.

    Parameters:
        data: pandas Series, shape (n_samples,). Input là giá close hoặc return.
        threshold: float, tùy chọn (mặc định = 3.5). Ngưỡng để xác định giá trị của outlier. Những điểm có giá trị với sai số tuyệt đối tính từ điểm trung vị lớn hơn giá trị ngưỡng * MAD thì được cho là outliers.
        figsize: tuple, tùy chọn (mặc định = (10, 8)). Kích thước của hình.

    Returns:
        Sơ đồ biểu diễn các outlier trong hình.

    """

    # Tính giá trị trung vị
    median = np.median(data)

    # Tính giá trị MAD
    mad = stats.median_abs_deviation(data)

    # Tính giá trị ngưỡng
    threshold_value = threshold * mad

    # Tìm các outlier
    outliers = []
    outliers_idx = []
    for idx, val in enumerate(data):
        if np.abs(val - median) > threshold_value:
            outliers.append(val)
            outliers_idx.append(data.index[idx])

    # Vẽ sơ đồ gốc cùng với các outlier đã được tìm thấy
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(data.index, data, color='b', label='Original Data')
    ax.scatter(outliers_idx, outliers, color='r', marker='x', label='Outliers')
    ax.set_ylabel('Value')
    ax.set_title('Time Series Data with Outliers Detected (MAD Method)')
    ax.legend()
    ax.grid(True)

    return fig, ax


def Seasonal_Decomposition(data, model={'additive', 'multiplicative'}, figsize=(10, 8), period=12):
    
    """
    Vẽ sơ đồ về seasonal decomposition.

    Parameters:
    data: pandas Series, shape (n_samples). Input là giá close hoặc return.
    model: {'additive', 'multiplicative'}, tùy chọn (mặc định = 'additive'). Mô hình seasonal decomposition muốn sử dụng.
    figsize: tuple, tùy chọn (mặc định = (10, 8)). Kích thước sơ đồ cần vẽ.
    period: int, tùy chọn. Chu kỳ của dữ liệu nếu có.

    Returns:
        Sơ đồ biểu diễn các thành phần của Seasonal Decomposition.

    """

    # Biến đổi seasonal decomposition
    result = seasonal_decompose(data, model=model, period=period)
    
    # Vẽ sơ đồ
    plt.subplot(411)
    plt.plot(result.observed, label='Observed')
    plt.legend(loc='best')

    plt.subplot(412)
    plt.plot(result.trend, label='Trend')
    plt.legend(loc='best')

    plt.subplot(413)
    plt.plot(result.seasonal, label='Seasonal')
    plt.legend(loc='best')

    plt.subplot(414)
    plt.plot(result.resid, label='Residual')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.show()
