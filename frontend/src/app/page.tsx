// frontend/src/app/page.tsx
'use client'
import { useQuery }    from '@tanstack/react-query'
import { fetchInsights } from '@/src/lib/api'
import { StatCards }   from '@/src/components/dashboard/StatCards'
import { RiskChart }   from '@/src/components/dashboard/RiskChart'
import { FraudTable }  from '@/src/components/dashboard/FraudTable'
import { Card, CardContent, CardHeader, CardTitle } from '@/src/components/ui/card'

// In production this comes from a DB or file upload
// For now we seed 20 test transactions
import { SAMPLE_TRANSACTIONS } from '@/src/lib/sampleData'

export default function DashboardPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['insights'],
    queryFn : () => fetchInsights(SAMPLE_TRANSACTIONS),
    refetchInterval: 30_000,   // auto-refresh every 30s
  })

  if (isLoading) return (
    <div className="flex items-center justify-center h-screen text-muted-foreground">
      Analyzing transactions...
    </div>
  )

  if (isError || !data) return (
    <div className="flex items-center justify-center h-screen text-red-500">
      Failed to load insights. Is the API running?
    </div>
  )

  return (
    <main className="max-w-7xl mx-auto px-6 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-medium">Financial behavior analyzer</h1>
        <p className="text-muted-foreground text-sm mt-1">
          {data.total_transactions} transactions analyzed
        </p>
      </div>

      <StatCards data={data} />

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">Risk distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <RiskChart breakdown={data.risk_breakdown} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base font-medium">Highest risk transactions</CardTitle>
          </CardHeader>
          <CardContent>
            <FraudTable rows={data.highest_risk} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base font-medium">All transactions</CardTitle>
        </CardHeader>
        <CardContent>
          <FraudTable rows={data.results} />
        </CardContent>
      </Card>
    </main>
  )
}