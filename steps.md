                                    
Step 2	Identify active subscriptions in Jan 2023 on Subscription Data table							Dependendent: Step 1	
Step 3	Identify Unique active customers in Jan 23 on Subscription Data table							Dependendent: Step 2	
Step 4	Identify customer status on Subscription Data table, Churned or Retained during the period      Dependendent: Step 3	
Step 5	Calculate Initial Plan Date on Subscription Data table								
Step 6	Find Initial Plan Type & Subscription Type on Subscription Data table							Dependendent: Step 5	
Step 7	Join Industry Segment and Acquisition Channel from Customer Data to Subscription Data table								
Step 8	Identify which orders belong to customers with active subscriptions in Jan 2023 on customer and order data      Dependendent: Step 2,3,4	
Step 9	Join "Unique Active Customers on Jan '23" column to Order and Customer Data tables								
Step 10	Join Initial Plan and Subscription Type from Subscription Table to Customer Table								
Step 11	Join Initial Plan, Subscription Type, acquisition channel, geography, industry, customer type from Customer Table to Order Table	        Dependendent: Step 10	
Step 12	Identify Active Jan 2023 Cohort customers who ordered in 2023 on Customer Data table								
                                    
Formulas/Functions:	If(and								
    If(countif								
    Minifs								
    Index(match				

Step 13	Create tables for Customer LTV by Initial Subscription & Plan					
    Create tables for Profit per User and Customer Churn metrics					
Step 14	Calculate churn rate, take unique active customers for the cohort					Dependent: Steps 2-12
    and divide by the number that churned in 2023					
Step 15	Calculate Profit per User metrics, get profit from order that belong to 					Dependent: Steps 2-12
    the cohort of customers who were active in Jan 2023 and ordered in 2023 and					
    divide by the number of customers who were active in jan 2023 and ordered in 2023					
Step 16	Calculate LTV, using formula if churn is 0 then take the assumption of 					Dependent: Steps 1, 14-15
    5 year churn rate and multiply it by profit per user, if its not then divide profit per user by churn					
Step 17	Repeat for LTV by other attributes					
                        
Formulas/Functions:	If					
    Sumifs					
    Countifs					
    Divide					
    Iferror									