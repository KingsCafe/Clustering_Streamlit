from math import log
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

#import datasets for further analysis
df = pd.read_csv(r'C:\Users\wkbmi\Desktop\TEMP\database\Ads.csv')

import streamlit as st
from sklearn.cluster import KMeans


st.header('Simple Clustering App')
st.subheader('Dataframe Details')
st.write('Table dimensions: ',df.shape)
st.dataframe(df.head())
st.write('Table missing values')
st.write(df.isna().sum())

#displaying distribution for each features
cat_var, num_var = st.beta_columns(2)
cat_ = cat_var.selectbox('categorical features:',df.select_dtypes(include='object').columns)
fig, ax = plt.subplots()
sns.countplot(df[cat_],ax=ax)
ax.set_title('Count of Categorical Feature')
cat_var.pyplot(fig)

num_ = num_var.selectbox('numerical features:',df.select_dtypes(exclude='object').columns)
fig, ax = plt.subplots()
sns.distplot(df[num_],ax=ax)
ax.set_title('Distribution for Each Feature')
num_var.pyplot(fig)

#conver categorical to numerical for machine training
df['Gender'] = df['Gender'].replace({'Male':1,'Female':0})
#displaying data info after converting
st.subheader('displaying converted dataset with all in numerical type for machine training')
st.write(df.head())

#we will be using only features Gender, Age, and Estimated Salary for clustering
x_train = df.iloc[:, 1:-1]

#comparing inertia reading for each cluster trained
inertia = []
for i in range(2,15):
    kmeans = KMeans(n_clusters=i, random_state=10)
    kmeans.fit(x_train)
    inertia.append(kmeans.inertia_)
inertia_df = pd.DataFrame({'cluster':range(2,15),'inertia':inertia})
fig, ax = plt.subplots()
ax.plot(inertia_df['cluster'],inertia_df['inertia'])
ax.set_title('Cluster vs Inertia Plot')
ax.set_xlabel('Cluster')
ax.set_ylabel('Inertia')
ax.annotate('cluster#5 will lesser loss will be used',xy=(5,inertia[3]),xytext=(8,inertia[1]),arrowprops={'arrowstyle':'->', 'color': 'red'})
st.pyplot(fig)

kmeans_5 = KMeans(n_clusters=5, random_state=10)
kmeans_5.fit(x_train)

#selecting features to plot a scatter graph displaying clusters
x_c, y_c = st.beta_columns(2)
st.subheader('Choose the Feature To Display on Plots')
x_cluster = st.selectbox('select x: ',x_train.columns)
y_cluster = st.selectbox('select y: ',x_train.columns)

fig, ax = plt.subplots()
sns.scatterplot(x_cluster,y_cluster,hue=kmeans_5.labels_,data=x_train,ax = ax)
ax.set_title('Clustering for Each Feature Using KMeans')
x_c.pyplot(fig)

#create a prediction function
from sklearn.ensemble import RandomForestClassifier

y_train = df.iloc[:,-1:]    
forest = RandomForestClassifier()
forest.fit(x_train, y_train)


fig, ax = plt.subplots()
sns.scatterplot(x_cluster, y_cluster,hue='Purchased',data=df, ax = ax)
ax.set_title('Features selection Vs target')
y_c.pyplot(fig)

def prediction(Gender, Age, EstimatedSalary):
    global predict
    if Gender == "Male":
        Gender = 1
    elif Gender == 'Female':
        Gender = 0
    
    predict = forest.predict([[Gender, Age, EstimatedSalary]])

    if predict == 0:
        return 'Will Not Purchase'
    else:
        return 'will Purchase'


def main():
    st.subheader('Enter Feature Characteristics For Prediction')
    Gender = st.selectbox('Gender',('Male','Female'))
    Age = st.number_input('Age',value=1)
    EstimatedSalary = st.number_input('Estimated Salary',value=1)
    result = ''

    if st.button('predict'):
        result = prediction(Gender, Age, EstimatedSalary)
        st.success('The customer {}'.format(result))
        st.write(predict)


if __name__ == '__main__':
    main()

