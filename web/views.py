
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.svm import SVC    
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
def home(request):
    return render(request,"home.html")
def predict(request):
    return render(request,"predict.html")
def Test(request):
    # df = pd.read_csv(r"D:\New\project2\diabetes.csv")
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv")
    # df = pd.read_csv
    df["Glucose"] = df['Glucose'].replace(0,df["Glucose"].mean())
    df["BloodPressure"] = df['BloodPressure'].replace(0,df["BloodPressure"].mean())
    df["SkinThickness"] = df['SkinThickness'].replace(0,df["SkinThickness"].mean())
    df["Insulin"] = df['Insulin'].replace(0,df["Insulin"].mean())
    df["BMI"] = df['BMI'].replace(0,df["BMI"].mean())
    cols_important = ["Glucose","BMI","Age","Pregnancies"]
    # cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
    #    'BMI', 'DiabetesPedigreeFunction', 'Age',]
    x = df[cols_important]
    y = df["Outcome"]
    z = StandardScaler()
    z.fit(x)
    zz = z.fit_transform(x)
    dz = pd.DataFrame(zz,columns=cols_important)
    xz = dz[cols_important]
    yz = df["Outcome"]

    # dz = pd.DataFrame(zz,columns=cols)

    # x_train , x_test , y_train , y_test = train_test_split(zz,y,test_size=0.2,random_state=7)

    
    model = LogisticRegression()
    model.fit(xz,yz)
    # model.score(x_test,y_test)
    d1 , d2 , d3 , d4 = int(request.GET["n1"]) , float(request.GET["n2"]) , int(request.GET["n3"]) , float(request.GET["n4"])
    n1 = (float(request.GET["n1"]) - df["Age"].mean()) / (df["Age"].std())
    n2 = (float(request.GET["n2"]) - df["BMI"].mean()) / (df["BMI"].std())
    n3 = (float(request.GET["n3"]) - df["Pregnancies"].mean()) / (df["Pregnancies"].std())
    n4 = (float(request.GET["n4"]) - df["Glucose"].mean()) / (df["Glucose"].std())
    #  cols_important = ["Glucose","BMI","Age","Pregnancies"]
    n = np.array([n4,n2,n1,n3])

    pred = model.predict([n])
    answer = ""
    if pred == [1]:
        answer = "ผล:คุณมีความเสี่ยงสูง"
    else:
        answer = "ผล:คุณมีความเสี่ยงต่ำ"

    return render(request,"predict.html",
        {"name":answer,
        "text1":d1,"text2":d2,"text3":d3,"text4":d4}
    )
def bmi(request):
    return render(request,"bmi.html")

def bmii(request):
    b1 , b2  = float(request.GET["bb1"]) , float(request.GET["bb2"])
    b1_edit = (b1/100)**2
    bmi_cal = b2 / b1_edit
    if bmi_cal >= 30:
        g = "ไอต้าวอ้วนมากๆเลย คุมอาหารด้วย"
    elif bmi_cal >= 25:
        g = "อ้วนแล้วน่ะ ออกกำลังกายเยอะๆ"
    elif bmi_cal >= 23:
        g = "เริ่มจะอ้วนแล้ว"
    elif bmi_cal >= 18.5:
        g = "ปกติดีแข็งแรง"
    else:
        g = "ผอม กินเยอะๆหน่อยน่ะ"
    bmi_cal = round(bmi_cal,2)
    bmi_cal = f"BMI:{bmi_cal}"
    return render(request,"bmi.html",
        {"bbb":bmi_cal,
        "text5":b1,"text6":b2,"aaa":g}
    )
