SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    s.price,
    ROUND(COALESCE(SUM(t.amount), 0), 2) AS total_revenue,
    COUNT(DISTINCT t.transaction_id) AS total_transactions,
    ROUND(AVG(p.active_users), 2) AS average_active_users,
    ROUND(AVG(p.sessions), 2) AS average_sessions,
    ROUND(AVG(p.features_used), 2) AS average_features_used
FROM customers c
LEFT JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
LEFT JOIN product_usage p
    ON c.customer_id = p.customer_id
GROUP BY
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    s.price
ORDER BY total_revenue DESC;


SELECT
    plan,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS average_revenue_per_customer,
    ROUND(AVG(average_active_users), 2) AS average_active_users,
    ROUND(AVG(average_sessions), 2) AS average_sessions
FROM (
    SELECT
        c.customer_id,
        s.plan,
        COALESCE(SUM(t.amount), 0) AS total_revenue,
        AVG(p.active_users) AS average_active_users,
        AVG(p.sessions) AS average_sessions
    FROM customers c
    LEFT JOIN subscriptions s
        ON c.customer_id = s.customer_id
    LEFT JOIN transactions t
        ON c.customer_id = t.customer_id
    LEFT JOIN product_usage p
        ON c.customer_id = p.customer_id
    GROUP BY
        c.customer_id,
        s.plan
) customer_metrics
GROUP BY plan
ORDER BY total_revenue DESC;


SELECT
    c.industry,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(t.amount), 2) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction_value
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.industry
ORDER BY total_revenue DESC;


SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(t.amount), 2) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction_value
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    ROUND(COALESCE(SUM(t.amount), 0), 2) AS total_revenue,
    ROUND(COALESCE(AVG(p.active_users), 0), 2) AS average_active_users,
    ROUND(COALESCE(AVG(p.sessions), 0), 2) AS average_sessions,
    ROUND(COALESCE(AVG(p.features_used), 0), 2) AS average_features_used
FROM customers c
LEFT JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
LEFT JOIN product_usage p
    ON c.customer_id = p.customer_id
GROUP BY
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status
ORDER BY
    average_active_users DESC,
    total_revenue DESC
LIMIT 20;