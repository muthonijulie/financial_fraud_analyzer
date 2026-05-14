export interface TransactionResult{
    index: number;
    amount: number;
    fraud_probability: number;
    is_fraud: boolean;
    risk_level:'low' | 'medium' | 'high';
}

export interface RiskBreakdown{
    low: number;
    medium: number;
    high: number;
}
export interface InsightsResponse{
    total_transactions: number;
    flagged_count: number;
    total_amount: number;
    flagged_amount: number;
    risk_breakdown: RiskBreakdown;
    highest_risk: TransactionResult[];
    avg_amount: number;
    avg_fraud_prob: number;
    results: TransactionResult[];
    fraud_rate_pct: number;
}