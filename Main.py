import openai
import time
import pandas as pd


inputCSV = pd.read_csv("TestCSV.csv")
APIKEY = open(r"C:\Users\beyou\Desktop\Token.txt","r")
#inputQuery = open("Test.txt", "r")
#result = open("result.txt", "a")

output = inputCSV.copy()
openai.api_key = APIKEY.readline()
#query = inputQuery.readlines()

queryCount = inputCSV['Sample'].count()
flag = 0
baseWait = 3
i = 0
queryPerSample = 2

while i < queryCount:
    query = inputCSV.loc[i, 'Sample']
    if flag != i:
        baseWait = 3 
    try:
        completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0,
        max_tokens = 500,
        messages = [
            {"role": "system", "content": "Your are an IB DP English teacher. You grade english writing samples following the IB DP English grading rubric from 2019"},
            {"role": "user", "content": "Grade the following sample strictly following the 2019 DP IB english grading rubric, be sure to give a grade out of 5 for every criteria while explaining why and give the final grade out of 5 and keep the total word count below 200. Then in a seperate response write a 20 word sentence giving your final thoughts on the sample."},
            {"role": "user", "content": query}
        ]   
        )
        
        resultDataFrame = pd.json_normalize(completion.choices[0].message)
        output.loc[i, 'Result'] = resultDataFrame['content'].loc[0]
        #result.write("Sample " + str(i + 1) + " \n" + str(completion.choices[0].message) + "\n")
        time.sleep(3)
    except Exception as e:
        print("Error with server on sample " + str(i + 1))
        print(e)
        if flag == i:
            baseWait = baseWait + 2
            
        flag = i
        i-= 1
        
        if baseWait > 13:
            print("Timeout on sample " + str(i + 1))
            break
        time.sleep(baseWait) 
    i+= 1


output.to_csv("outputCSV.csv") 

#result.close()
APIKEY.close()
#inputQuery.close()