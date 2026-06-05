!pip install pymssql
import pymssql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer


_server = '45.117.83.230'
_port = 1433
_user = 'Student_DA_Q1'
_pass = '@MindXDream2023'
_db = 'DA_FINAL_TEST'

conn = pymssql.connect(
    host=_server,
    port=_port,
    user=_user,
    password=_pass,
    database=_db
)

df = pd.read_sql('select * from [dbo].[Customer_Churn_Banker]', conn)
df

df.info()

df.churn.value_counts()

print(df.isnull().sum())

df.describe(include='all')

!pip install ydata_profiling
from ydata_profiling import ProfileReport
profile = ProfileReport(df, title="Profiling Report")
profile

fig, axes = plt.subplots(ncols=3, nrows=3, figsize= (20,15))

for col, ax in zip(df, axes.flat):
    sns.histplot(df[col], ax=ax)
plt.show()
df[df.columns].describe()

# phân thích thêm về balance: khách có số dư thấp có rời bỏ không?
sns.boxplot(data=df, x='churn', y='balance')
plt.title('Số dư tài khoản theo trạng thái rời bỏ')
plt.xlabel('Churn')
plt.ylabel('balance')
plt.show()


df.groupby('churn')['balance'].describe()

# mối liên hệ giữa tuổi và churn
sns.boxplot(x='churn', y='age', data=df)
plt.title("Độ tuổi theo trạng thái rời bỏ")
plt.show()

df.groupby('churn')['age'].describe()

# So sánh tỷ lệ churn giữa nam và nữ
sns.countplot(data=df, x='gender', hue='churn')
plt.title("Tỷ lệ churn giữa nam và nữ")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

churn_by_gender = df.groupby('gender')['churn'].mean()
print(churn_by_gender)

# So sánh tỷ lệ rời bỏ ở các quốc gia
sns.countplot(data=df, x='country', hue='churn')
plt.title("Tỷ lệ churn ở các quốc gia")
plt.xlabel("Country")
plt.ylabel("Count")
plt.show()

df.groupby('country')['churn'].mean().sort_values(ascending=False)

# So sánh tỷ lệ rời bỏ với khách hàng có credit_score
sns.boxplot(x='churn', y='credit_score', data=df)
plt.title("Tỷ lệ churn với credit_score")
plt.show()

df.groupby('churn')['credit_score'].describe()

# Khách có credit_card có rời bỏ không ?
sns.countplot(data=df, x='credit_card', hue='churn')
plt.title("Tỷ lệ churn với credit_card")
plt.show()

# Khách không hoạt động churn cao hơn hay ngược lại ?
sns.countplot(data=df, x='active_member', hue='churn')
plt.title("Tỷ lệ churn với active_member")
plt.show()

# Tenure có ảnh hưởng gì đến churn không?
sns.boxplot(x='churn', y='tenure', data=df)
plt.title("Tỷ lệ churn với tenure")
plt.show()

df.groupby('churn')['tenure'].describe()


# kiểm tra outlier by churn
num_cols = ['credit_score', 'age', 'tenure', 'balance', 'products_number', 'estimated_salary']

for col in num_cols:
    plt.figure(figsize=(8, 4))
    sns.boxplot(data=df, x='churn', y=col)
    plt.title(f"Boxplot of {col} by Churn")
    plt.xlabel("Churn")
    plt.ylabel(col)
    plt.show()

sns.countplot(data=df, x='churn')
plt.title("Số lượng khách hàng rời bỏ vs. ở lại")
plt.xlabel("Churn (0 = Ở lại, 1 = Rời bỏ)")
plt.ylabel("Số lượng khách hàng")
plt.show()

df.churn.value_counts()
X
y

from sklearn.preprocessing import OneHotEncoder, StandardScaler

# preprocessing
X = df.drop(columns='churn').reset_index(drop=True)
y = df.churn

# Label encode gender
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})


# 1HEncoder cột country
_enc = OneHotEncoder(sparse_output=False)
_enc.fit(X[['country']])
_transformed = pd.DataFrame(_enc.transform(X[['country']]), columns=_enc.get_feature_names_out())

# concat
X.drop(columns='country', inplace=True)
X = pd.concat([X, _transformed], axis=1)
X

X.drop(columns=['customer_id'], inplace=True) # drop cột customer_id vì không cần thiết
X

# scaler
_scaler = StandardScaler()
_scaler.fit(X)
X = pd.DataFrame(_scaler.transform(X), columns=X.columns)
X

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, recall_score
from sklearn.linear_model import LogisticRegression

!pip install imblearn
from imblearn.over_sampling import SMOTE

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

_imb = SMOTE()
X_train_resample, y_train_resample = _imb.fit_resample(X_train, y_train)

y_train.value_counts()

y_train_resample.value_counts()

print(X.columns)


# thử mô hình logistic với no resampling
_model = LogisticRegression()
_model.fit(X_train, y_train)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình XGBClassifier với no resampling
from xgboost import XGBClassifier
_model = XGBClassifier()
_model.fit(X_train, y_train)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình RandomForest với no resampling
from sklearn.ensemble import RandomForestClassifier
_model = RandomForestClassifier()
_model.fit(X_train, y_train)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình DecisionTree với no resampling
from sklearn.tree import DecisionTreeClassifier
_model = DecisionTreeClassifier()
_model.fit(X_train, y_train)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình logisticRegression (oversampling)
_model = LogisticRegression()
_model.fit(X_train_resample, y_train_resample)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# oversampling mô hình XGBClassifier
from xgboost import XGBClassifier
_model = XGBClassifier()
_model.fit(X_train_resample, y_train_resample)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình RandomForest với oversampling
from sklearn.ensemble import RandomForestClassifier
_model = RandomForestClassifier()
_model.fit(X_train_resample, y_train_resample)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)

# thử mô hình DecissionTree với oversampling
from sklearn.tree import DecisionTreeClassifier
_model = DecisionTreeClassifier()
_model.fit(X_train_resample, y_train_resample)
y_pred = _model.predict(X_test)

print(classification_report(y_true=y_test, y_pred=y_pred))
ConfusionMatrixDisplay.from_predictions(y_true=y_test, y_pred=y_pred)
