// frontend/src/components/dashboard/FraudTable.tsx
import { Badge } from '@/src/components/ui/badge'
import { TransactionResult } from '@/src/types/insights'

const riskColor = {
  LOW   : 'bg-green-100 text-green-800',
  MEDIUM: 'bg-yellow-100 text-yellow-800',
  HIGH  : 'bg-red-100 text-red-800',
}

export function FraudTable({ rows }: { rows: TransactionResult[] }) {
  return (
    <div className="overflow-x-auto rounded-lg border">
      <table className="w-full text-sm">
        <thead className="bg-muted text-muted-foreground">
          <tr>
            {['#', 'Amount', 'Fraud prob', 'Risk', 'Verdict'].map(h => (
              <th key={h} className="px-4 py-3 text-left font-medium">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.index}
              className={`border-t ${r.is_fraud ? 'bg-red-50 dark:bg-red-950/20' : ''}`}>
              <td className="px-4 py-2 text-muted-foreground">{r.index}</td>
              <td className="px-4 py-2">${r.amount.toFixed(2)}</td>
              <td className="px-4 py-2 font-mono">
                {(r.fraud_probability * 100).toFixed(2)}%
              </td>
              <td className="px-4 py-2">
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium
                  ${riskColor[r.risk_level.toUpperCase() as keyof typeof riskColor]}`}>
                  {r.risk_level}
                </span>
              </td>
              <td className="px-4 py-2">
                {r.is_fraud
                  ? <Badge variant="destructive">Fraud</Badge>
                  : <Badge variant="outline">Legit</Badge>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}