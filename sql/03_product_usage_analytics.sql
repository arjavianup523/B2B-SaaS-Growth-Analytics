SELECT
    COUNT(*) AS total_usage_records
FROM product_usage;


SELECT
    COUNT(DISTINCT customer_id) AS customers_using_product
FROM product_usage;


SELECT
    SUM(active_users) AS total_active_users
FROM product_usage;


SELECT
    ROUND(AVG(active_users), 2) AS average_active_users
FROM product_usage;


SELECT
    ROUND(AVG(sessions), 2) AS average_sessions
FROM product_usage;


SELECT
    ROUND(AVG(features_used), 2) AS average_features_used
FROM product_usage;


SELECT
    usage_month,
    SUM(active_users) AS total_active_users,
    SUM(sessions) AS total_sessions,
    SUM(features_used) AS total_features_used
FROM product_usage
GROUP BY usage_month
ORDER BY usage_month;


SELECT
    customer_id,
    ROUND(AVG(active_users), 2) AS average_active_users,
    ROUND(AVG(sessions), 2) AS average_sessions,
    ROUND(AVG(features_used), 2) AS average_features_used
FROM product_usage
GROUP BY customer_id
ORDER BY average_active_users DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM customers c
JOIN product_usage p
    ON c.customer_id = p.customer_id
GROUP BY
    c.customer_id,
    c.company_name,
    c.industry,
    c.country
ORDER BY average_active_users DESC;


SELECT
    s.plan,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM subscriptions s
JOIN product_usage p
    ON s.customer_id = p.customer_id
GROUP BY s.plan
ORDER BY average_active_users DESC;


SELECT
    s.status,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM subscriptions s
JOIN product_usage p
    ON s.customer_id = p.customer_id
GROUP BY s.status
ORDER BY average_active_users DESC;


SELECT
    c.industry,
    COUNT(DISTINCT p.customer_id) AS customers,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM customers c
JOIN product_usage p
    ON c.customer_id = p.customer_id
GROUP BY c.industry
ORDER BY average_active_users DESC;


SELECT
    c.country,
    COUNT(DISTINCT p.customer_id) AS customers,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM customers c
JOIN product_usage p
    ON c.customer_id = p.customer_id
GROUP BY c.country
ORDER BY average_active_users DESC;


SELECT
    p.customer_id,
    c.company_name,
    s.plan,
    s.status,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM product_usage p
JOIN customers c
    ON p.customer_id = c.customer_id
JOIN subscriptions s
    ON p.customer_id = s.customer_id
GROUP BY
    p.customer_id,
    c.company_name,
    s.plan,
    s.status
ORDER BY average_active_users DESC
LIMIT 20;