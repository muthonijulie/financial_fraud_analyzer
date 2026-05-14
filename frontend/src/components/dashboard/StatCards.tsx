import { Card, CardContent } from '@/src/components/ui/card'
import { InsightsResponse } from '@/src/types/insights'
import { ShieldAlert, DollarSign, Activity, TrendingUp } from 'lucide-react'

interface Props { data: InsightsResponse }

export function StatCards({ data }: Props) {
  const stats = [
    {
      label: 'Total transactions',
      value: data.total_transactions.toLocaleString(),
      icon : <Activity size={18} />,
    },
    {
      label: 'Flagged as fraud',
      value: data.flagged_count.toLocaleString(),
      icon : <ShieldAlert size={18} />,
      alert: data.flagged_count > 0,
    },
    {
      label: 'Fraud rate',
      value: `${data.fraud_rate_pct}%`,
      icon : <TrendingUp size={18} />,
    },
    {
      label: 'Total amount',
      value: `$${data.total_amount.toLocaleString()}`,
      icon : <DollarSign size={18} />,
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((s) => (
        <Card key={s.label}
          className={s.alert ? 'border-red-400' : ''}>
          <CardContent className="pt-5">
            <div className="flex items-center gap-2 text-muted-foreground mb-1">
              {s.icon}
              <span className="text-sm">{s.label}</span>
            </div>
            <p className={`text-2xl font-medium
              ${s.alert ? 'text-red-500' : ''}`}>
              {s.value}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}