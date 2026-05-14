import { InsightsResponse } from '@/src/types/insights'
const BASE=''

export async function fetchInsights(
    transactions:Record<string,number>[]
):Promise<InsightsResponse>{
    const res=await fetch(`${BASE}/api/v1/insights`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({transactions})
    })

    if(!res.ok) throw new Error(`API error:${res.status}`)
        return res.json()
}
