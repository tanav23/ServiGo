USE servigo;
SELECT DATABASE() AS Current_Database;
SHOW TABLES;
SELECT COUNT(*) AS Total_Orders
FROM orders;
SELECT COUNT(*) AS Orders_Rows
FROM orders;
SELECT COUNT(*) AS Staging_Rows
FROM orders_stage;
DESCRIBE orders_stage;
CREATE TABLE IF NOT EXISTS orders_stage_text (
    Order_ID TEXT,
    Customer_ID TEXT,
    City TEXT,
    Category TEXT,
    Booking_Date TEXT,
    Scheduled_Date TEXT,
    Partner_ID TEXT,
    Order_Status TEXT,
    Cancellation_Reason TEXT,
    Completion_Date TEXT,
    Service_Duration_Min TEXT,
    Response_Time_Min TEXT,
    Price TEXT,
    Discount TEXT,
    Revenue TEXT,
    Customer_Rating TEXT,
    Complaint_Flag TEXT,
    Rework_Flag TEXT,
    Assignment_Status TEXT,
    Repeat_Booking_Flag TEXT,
    Order_Month TEXT,
    Order_Delay_Days TEXT,
    Service_Completed_Flags TEXT,
    Order_Cancelled_Flag TEXT,
    Order_NoShow_Flag TEXT,
    Order_Assigned_Flag TEXT,
    Partner_Cancelled_Flag TEXT,
    Customer_Cancelled_Flag TEXT,
    Supply_Failure_Flag TEXT,
    Scheduling_Issue_Flag TEXT,
    Discount_Rate TEXT,
    High_ResponseTime_Flag TEXT,
    Service_Duration_Hours TEXT,
    Signup_Date TEXT,
    Signup_Channel TEXT,
    Partner_Name TEXT,
    Join_Date TEXT,
    Experience_Level TEXT,
    Initial_Quality_Score TEXT,
    Initial_Rating TEXT,
    Partner_Tenure_Months TEXT,
    Partner_Tenure_Group TEXT,
    Application_Date TEXT,
    Verification_Date TEXT,
    Verification_Status TEXT,
    Skill_Assessment_Date TEXT,
    Training_Date TEXT,
    Training_Status TEXT,
    Quality_Check_Date TEXT,
    Initial_Quality_Check TEXT,
    Activation_Date TEXT,
    Activation_Status TEXT,
    Onboarding_Status TEXT,
    Active_Status TEXT
);
SHOW TABLES;
SHOW VARIABLES LIKE 'local_infile';
SELECT COUNT(*) AS Total_Orders
FROM orders;
SELECT
    SUM(Completion_Date IS NULL) AS Missing_Completion_Dates,
    SUM(Service_Duration_Min IS NULL) AS Missing_Service_Durations,
    SUM(Customer_Rating IS NULL) AS Missing_Customer_Ratings
FROM orders;
SELECT
    COUNT(*) AS Total_Orders,

    SUM(
        CASE
            WHEN Order_Status = 'Completed' THEN 1
            ELSE 0
        END
    ) AS Completed_Orders,

    SUM(
        CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS Cancelled_Orders,

    SUM(
        CASE
            WHEN Order_Status = 'No-Show' THEN 1
            ELSE 0
        END
    ) AS No_Show_Orders,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN Order_Status = 'Completed' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS Completion_Rate_Pct,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN Order_Status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS Cancellation_Rate_Pct,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN Order_Status = 'No-Show' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS No_Show_Rate_Pct

FROM orders;
SELECT
    Cancellation_Reason,
    COUNT(*) AS Cancelled_Orders,
    ROUND(
        100.0 * COUNT(*)/
        (
            SELECT COUNT(*)
            FROM orders
            WHERE Order_Status = 'Cancelled'
        
    ),
    2) AS Pct_Of_Cancellations
FROM orders
WHERE Order_Status = 'Cancelled'
GROUP BY Cancellation_Reason
ORDER BY Cancelled_Orders DESC;
SELECT
    City,
    COUNT(*) AS Total_Orders,
    SUM(Order_Status = 'Cancelled') AS Cancelled_Orders,
    ROUND(
        100.0*SUM(Order_Status = 'Cancelled')
        / NULLIF(COUNT(*), 0),
        2
    ) AS Cancellation_Rate_Pct,
    SUM(Cancellation_Reason = 'No Partner Available') AS Supply_Failure_Orders,
    ROUND(
        100.0*SUM(Cancellation_Reason = 'No Partner Available')
        / NULLIF(COUNT(*),0),
        2
    ) AS Supply_Failure_Rate_Pct 
FROM orders
GROUP BY City 
ORDER BY Cancellation_Rate_Pct DESC;
SELECT
    City,
    Category,
    COUNT(*) AS Total_Orders,
    SUM(
        Cancellation_Reason = 'No Partner Available'
    ) AS Supply_Failure_Orders,
    ROUND(
        100.0 * SUM(
            Cancellation_Reason = 'No Partner Available'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS Supply_Failure_Rate_Pct,
    ROUND(
        100.0 * SUM(
            Order_Status = 'Cancelled'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS Cancellation_Rate_Pct
FROM orders
GROUP BY City, Category
ORDER BY
    Supply_Failure_Rate_Pct DESC,
    Supply_Failure_Orders DESC;
SELECT
    City,
    Category,
    Order_month,
    COUNT(*) AS Total_Orders,
    SUM(
        Cancellation_Reason = 'No Partner Available' 
    ) AS Supply_Failure_Orders,
    ROUND(
        100.0*SUM(Cancellation_Reason = 'No Partner Available'
    )/ NULLIF(COUNT(*),0),
    2) AS Supply_Failure_Rate_Pct
FROM orders
WHERE
    (City = 'Delhi NCR'
        AND Category = 'AC & Appliance Repair')
    OR
    (City = 'Mumbai'
        AND Category = 'Cleaning & Pest Control')
    OR
    (City = 'Bengaluru'
        AND Category = 'Electricians')
GROUP BY 
    City,
    Category,
    Order_Month
ORDER BY
    City,
    Category,
    Order_Month;
USE servigo;
CREATE TABLE IF NOT EXISTS availability_monthly(
    Partner_ID VARCHAR(20),
    Availability_Month VARCHAR(7),
    Total_Available_Hours DOUBLE,
    Total_Booked_Hours DOUBLE,
    Monthly_Utilization_Rate DOUBLE
);
SELECT
    o.City,
    o.Category,
    COUNT(*) AS Total_Orders,
    SUM(
        o.Cancellation_Reason = 'No Partner Available'
    ) AS Supply_Failure_Orders,
    ROUND(
        100.0*SUM(
            o.Cancellation_Reason = 'No Partner Available'
        )/ NULLIF(COUNT(*), 0),
        2
    ) AS Supply_Failure_Rate_Pct,
     COUNT(DISTINCT a.Partner_ID) AS Partners_Observed,
    ROUND(
        100.0 * SUM(a.Total_Booked_Hours)
        / NULLIF(SUM(a.Total_Available_Hours), 0),
        2
    ) AS Utilization_Rate_Pct
FROM orders o
LEFT JOIN availability_monthly a
    ON o.Partner_ID = a.Partner_ID
    AND o.Order_Month = a.Availability_Month
WHERE
    (o.City = 'Delhi NCR'
        AND o.Category = 'AC & Appliance Repair')
    OR
    (o.City = 'Mumbai'
        AND o.Category = 'Cleaning & Pest Control')
    OR
    (o.City = 'Bengaluru'
        AND o.Category = 'Electricians')
GROUP BY
    o.City,
    o.Category
ORDER BY
    Supply_Failure_Rate_Pct DESC;
SELECT
    p.City,
    p.Category,
    COUNT(DISTINCT a.Partner_ID) AS Partners_Observed,
    ROUND(SUM(a.Total_Available_Hours), 2)
        AS Total_Available_Hours,
    ROUND(SUM(a.Total_Booked_Hours), 2)
        AS Total_Booked_Hours,
    ROUND(
        100.0 * SUM(a.Total_Booked_Hours)
        / NULLIF(SUM(a.Total_Available_Hours), 0),
        2
    ) AS Utilization_Rate_Pct
FROM availability_monthly a
JOIN (
    SELECT DISTINCT
        Partner_ID,
        City,
        Category
    FROM orders
    WHERE Partner_ID IS NOT NULL
) p
    ON a.Partner_ID = p.Partner_ID
GROUP BY
    p.City,
    p.Category
ORDER BY
    Utilization_Rate_Pct DESC;
SELECT
    ROUND(SUM(Total_Available_Hours), 2)
        AS Total_Available_Hours,
    ROUND(SUM(Total_Booked_Hours), 2)
        AS Total_Booked_Hours,
    ROUND(
        100.0 * SUM(Total_Booked_Hours)
        / NULLIF(SUM(Total_Available_Hours), 0),
        2
    ) AS Overall_Utilization_Rate_Pct
FROM availability_monthly;
SELECT
    Partner_ID,
    Partner_Name,
    City,
    Category,
    COUNT(*) AS Assigned_Orders,
    SUM(
        Order_Status = 'Completed'
    ) AS Completed_Orders,
    ROUND(
        100.0*SUM(Order_Status='Completed'
        )/ NULLIF(COUNT(*), 0),
    2) AS Completion_Rate_Pct,
    ROUND(
        AVG(
            CASE
                WHEN Order_Status="Completed"
                THEN Customer_Rating
            END),
    2) AS Avg_Custonmer_Rating,
    SUM(
        CASE
            WHEN Order_Status='Completed'
                AND Complaint_Flag=1
            THEN 1
            ELSE 0
        END
    ) AS Complaint_Orders,
    ROUND(
        100.0*SUM(
            CASE
                WHEN Order_Status='Completed'
                    AND Complaint_Flag=1
                THEN 1
                ELSE 0
            END
        )/ NULLIF(SUM(Order_Status='Completed'),0),
    2) AS Complaint_Rate_Pct,
    ROUND(
        SUM(Revenue),
    2) AS Partner_Revenue,
    ROUND(
        AVG(Response_Time_Min),
    2) AS Avg_Response_Time_Min
FROM orders
WHERE Partner_ID IS NOT NULL
GROUP BY
    Partner_ID,
    Partner_Name,
    City,
    Category
HAVING SUM(Order_Status='Completed')>=10
ORDER BY
    Completed_Orders DESC;
SELECT
    Partner_ID,
    Partner_Name,
    City,
    Category,
    COUNT(*) AS Assigned_Orders,
    SUM(
        Order_Status = 'Completed'
    ) AS Completed_Orders,
    ROUND(
        100.0*SUM(Order_Status='Completed'
        )/ NULLIF(COUNT(*), 0),
    2) AS Completion_Rate_Pct,
    ROUND(
        AVG(
            CASE
                WHEN Order_Status='Completed'
                THEN Customer_Rating
            END
        ),
    2) AS Avg_Customer_Rating,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Order_Status='Completed'
                    AND Complaint_Flag=1
                THEN 1
                ELSE 0
            END
        ) / NULLIF(SUM(Order_Status='Completed'), 0),
    2) AS Complaint_Rate_Pct,
    ROUND(AVG(Response_Time_Min), 2)
        AS Avg_Response_Time_Min

FROM orders
WHERE Partner_ID IS NOT NULL
GROUP BY
    Partner_ID,
    Partner_Name,
    City,
    Category
HAVING SUM(Order_Status = 'Completed') >= 10
ORDER BY
    Completion_Rate_Pct ASC,
    Avg_Customer_Rating ASC;
SELECT
    Experience_Level,
    COUNT(DISTINCT Partner_ID) AS Total_Partners,
    COUNT(*) AS Assigned_Orders,
    SUM(Order_Status='Completed') AS Completed_Orders,
    ROUND(
        100.0*SUM(Order_Status='Completed')
        / NULLIF(COUNT(*),0),
    2) AS Completion_Rate_Pct,
    ROUND(
        AVG(
            CASE
                WHEN Order_Status='Completed'
                THEN Customer_Rating
            END
        ),2
    ) AS Avg_Customer_Rating,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN Order_Status = 'Completed'
                 AND Complaint_Flag = 1
                THEN 1 ELSE 0
            END
        )
        / NULLIF(
            SUM(Order_Status = 'Completed'), 0
        ),
        2
    ) AS Complaint_Rate_Pct

FROM orders
WHERE Partner_ID IS NOT NULL
GROUP BY Experience_Level
ORDER BY Completion_Rate_Pct DESC;
SELECT
    Complaint_Flag,
    Rework_Flag,
    COUNT(*) AS Completed_Orders,

    ROUND(
        AVG(Customer_Rating),
        2
    ) AS Avg_Customer_Rating,

    ROUND(
        100.0 * SUM(Rework_Flag = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS Rework_Rate_Pct

FROM orders
WHERE Order_Status = 'Completed'
GROUP BY Complaint_Flag, Rework_Flag
ORDER BY Avg_Customer_Rating;
SELECT
    Customer_Order_Group,
    COUNT(*) AS Total_Orders,
    COUNT(DISTINCT Customer_ID) AS Unique_Customers,

    ROUND(
        100.0 * SUM(Order_Status = 'Completed')
        / NULLIF(COUNT(*), 0),
        2
    ) AS Completion_Rate_Pct,

    ROUND(
        AVG(
            CASE
                WHEN Order_Status = 'Completed'
                THEN Customer_Rating
            END
        ),
        2
    ) AS Avg_Customer_Rating,

    ROUND(
        100.0 * SUM(Complaint_Flag = 1)
        / NULLIF(COUNT(*), 0),
        2
    ) AS Complaint_Rate_Pct
FROM(
    SELECT
        o.*,
        CASE
            WHEN COUNT(*) OVER(
                PARTITION BY Customer_ID
            )=1
            THEN 'One-Time Customer'
            ELSE 'Repeat Customer'
        END AS Customer_Order_Group
    FROM orders o
) AS customers_orders
GROUP BY Customer_Order_Group
ORDER BY Customer_Order_Group;
SELECT
    COUNT(DISTINCT Partner_ID) AS Total_Partners,

    COUNT(DISTINCT CASE
        WHEN Verification_Status = 'Passed'
        THEN Partner_ID
    END) AS Verification_Passed,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN Verification_Status = 'Passed'
            THEN Partner_ID
        END) / NULLIF(COUNT(DISTINCT Partner_ID), 0),
        2
    ) AS Verification_Rate_Pct,

    COUNT(DISTINCT CASE
        WHEN Training_Status = 'Completed'
        THEN Partner_ID
    END) AS Training_Completed,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN Training_Status = 'Completed'
            THEN Partner_ID
        END) / NULLIF(COUNT(DISTINCT Partner_ID), 0),
        2
    ) AS Training_Rate_Pct,

    COUNT(DISTINCT CASE
        WHEN Activation_Status = 'Activated'
        THEN Partner_ID
    END) AS Activated_Partners,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN Activation_Status = 'Activated'
            THEN Partner_ID
        END) / NULLIF(COUNT(DISTINCT Partner_ID), 0),
        2
    ) AS Activation_Rate_Pct

FROM orders
WHERE Partner_ID IS NOT NULL;
SELECT
    City,
    Cancellation_Reason,
    COUNT(*) AS Cancelled_Orders,

    ROUND(
        100.0 * COUNT(*)
        / NULLIF(
            SUM(COUNT(*)) OVER (PARTITION BY City),
            0
        ),
        2
    ) AS Pct_Of_City_Cancellations

FROM orders
WHERE Order_Status = 'Cancelled'
GROUP BY
    City,
    Cancellation_Reason
ORDER BY
    City,
    Cancelled_Orders DESC;

