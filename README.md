# Insurance All

Car Insurance Cross-Sell

![image](https://user-images.githubusercontent.com/72954917/133703422-1bc27912-6d98-4115-b1dc-87b9b5630463.png)-

# 1. Business Problem

**Company Name:** Insurance All

**Product/Service:** Offer Health Insurance

**Business Model:** An insurance policy is an arrangement by which a company undertakes to provide a guarantee of compensation for specified loss, damage, illness, or death in return for the payment of a specified premium. A premium is a sum of money that the customer needs to pay regularly to an insurance company for this guarantee.

source: https://www.relakhs.com/insurance-companies-business-model/

**Current Situation:** Now they want to offer car insurance. Last year they did a research with their 380 thousand customers about their interest in getting car insurance, and the results has been storage in a database together with others customers attributes.
The product team selected 127 thousand leads to participate in a marketing campaing that will be offering the new car insurance to them. The campaing will be made through phone calls by the sales team.

**Problem:** The problem is that the sales team has capacity of making only 20 thousand calls on the period the campaing will be running.
   
# 2. Business Assumptions
For the purpose of this project, I am going to assume the following:
- The cost per phone call: BRL 100.00
- Profit per convertion: BRL 31,699.00 (which is the median of annual premium charged of those 380 thousand customers)

# 3. Solution Strategy
My solution to solve the problem was:

**Step 01. Data Description:** Use basic statistics metrics to identify data outside the scope of business.

**Step 02. Check Outliers:** Check if there are outliers on the dataset based on the assumptions cited previously.

**Step 03. Feature Engineering:** Derive new features from the original dataset that could help to predict the likelihood of interest in car insurance.

**Step 04. Exploratory Data Analysis:** Explore the data to find insights and better understand the impact of variables on model learning.

**Step 05. Data Preparation:** Prepare the data to be used on the model. (Exe: Scaling, encoding)

**Step 06. Feature Selection:** Select features that are most significant that better explain the phenomenon.

**Step 07. Machine Learning:** Train and test models and analysis of the models performance.

**Step 08. Cross Validation Scoring:** Compare the performance of the models through cross validation and selection of the best model.

**Step 09. Hyperparameter Fine Tuning:** Choose the best parameters of the model that maximize performance.

**Step 10. Translation and Interpretation of the Error:** Convert the performance of the machine learning model into business results.

**Step 11. Deploy Model to Production:** Publish the model in a cloud environment so that other people or services can use the results to improve the business decision.

# 4. Top 3 Insights

# 5. Machine Learning Model Performance
The following machine learning models were trained:

- K Neighbors Classifier - KNN
- Logistic Regression
- Random Forest Classifier
- Adaboost
- Bagging Classifier

The performance of the models were measured through Cross Validation.

The metric that were employed to measure the performance of the models were **recall at k (recall@k)**, where k is the top k leads with the higher propensity score given by the model.

The following results were calculated with k=5,000

![image](https://user-images.githubusercontent.com/72954917/133708205-8cc3b4d5-f890-43ef-adb7-fdd9867396ad.png)

With these performances I chose Adaboost model, given that it presented the best recall_at_5000

![image](https://user-images.githubusercontent.com/72954917/133708717-d6b459b1-a15c-4026-9e9a-5232c5272ef5.png)

The performance curves show that the model can reach all of those interested in purchasing the product using approximately 50% of the sample (Cumulative Gains Curve). Furthermore, we can also see that the model is almost three times better with the first 20% of the sample in reaching interested customers than a random choosing technique. After reaching half of the data, it remains twice as good as the alternative way of classification.

# 6. Business Results

The table below shows us that calling for 20.000 random leads the company would reach around 20.42% customers that have interest in car insurance, on the other hand, with the model, calling the top 20.000 leads with the highest propensity score, the company would reach 58.52% customers that have interest in car insurance (increase of 37.83%).

Scenarios | Baseline | Model | Improvement
--- | --- | --- | ---
20.000 Calls | 20.42% | 58.52%  | 37.83% 
40.000 Calls | 41.52% | 93.71% | 52.19%

This next table below shows us the expected profit made by the company choosing random clientes to call and using the model to call for the top 20.000 and 40.000 leads, and the 

Scenarios | Baseline | Model | Improvement
--- | --- | --- | ---
20.000 Calls | BRL 73,435,558 | BRL 214,172,594 | BRL 140,737,036
40.000 Calls | BRL 149,372,967 | BRL 342,173,839 | BRL 192,800,872

# 7. Closing Thoughts

# 8. Lessons Learned

# 10. Next Steps to Improve


Ongoing project (13/09/2021)
