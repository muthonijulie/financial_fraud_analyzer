// frontend/src/components/dashboard/RiskChart.tsx
'use client'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { RiskBreakdown } from '@/src/types/insights'

const COLORS = {
  LOW   : '#1D9E75',
  MEDIUM: '#EF9F27',
  HIGH  : '#E24B4A',
}

export function RiskChart({ breakdown }: { breakdown: RiskBreakdown }) {
  const data = [
    { name: 'Low',    value: breakdown.low    },
    { name: 'Medium', value: breakdown.medium },
    { name: 'High',   value: breakdown.high   },
  ]

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie data={data} dataKey="value" cx="50%" cy="50%"
          innerRadius={60} outerRadius={100} paddingAngle={3}>
          {data.map((entry) => (
            <Cell key={entry.name}
              fill={COLORS[entry.name.toUpperCase() as keyof typeof COLORS]} />
          ))}
        </Pie>
        <Tooltip formatter={(v) => [v || 0, 'transactions']} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}