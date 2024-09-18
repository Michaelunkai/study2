'use client'

import { useState, useEffect } from 'react'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { motion } from "framer-motion"
import { Slider } from "@/components/ui/slider"
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

export default function EnhancedPricingCalculator() {
  const [seats, setSeats] = useState(1)
  const [usage, setUsage] = useState(0)
  const [discount, setDiscount] = useState('0')
  const [total, setTotal] = useState(0)
  const [isYearly, setIsYearly] = useState(false)

  const basePrice = 10 // Price per seat
  const usageRate = 0.05 // Price per unit of usage
  const yearlyDiscount = 0.1 // 10% discount for yearly billing

  useEffect(() => {
    const seatCost = seats * basePrice
    const usageCost = usage * usageRate
    const subtotal = seatCost + usageCost
    const discountAmount = subtotal * (parseInt(discount) / 100)
    let finalTotal = subtotal - discountAmount
    if (isYearly) {
      finalTotal = finalTotal * 12 * (1 - yearlyDiscount)
    }
    setTotal(finalTotal)
  }, [seats, usage, discount, isYearly])

  const pieData = [
    { name: 'Seat Cost', value: seats * basePrice },
    { name: 'Usage Cost', value: usage * usageRate },
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

  return (
    <Card className="w-full max-w-4xl mx-auto bg-gradient-to-br from-gray-900 to-gray-800 text-white shadow-xl">
      <CardHeader className="space-y-1">
        <CardTitle className="text-3xl font-extrabold">SaaS Pricing Calculator</CardTitle>
        <CardDescription className="text-gray-400">Calculate your custom pricing based on seats, usage, and discounts</CardDescription>
      </CardHeader>
      <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="seats" className="text-lg">Number of Seats</Label>
            <Slider
              id="seats"
              min={1}
              max={100}
              step={1}
              value={[seats]}
              onValueChange={(value) => setSeats(value[0])}
              className="w-full"
            />
            <div className="text-right text-2xl font-bold">{seats}</div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="usage" className="text-lg">Monthly Usage (units)</Label>
            <Input
              id="usage"
              type="number"
              min="0"
              value={usage}
              onChange={(e) => setUsage(Math.max(0, parseInt(e.target.value) || 0))}
              className="bg-gray-700 border-gray-600 text-white"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="discount" className="text-lg">Discount Tier</Label>
            <Select value={discount} onValueChange={setDiscount}>
              <SelectTrigger id="discount" className="bg-gray-700 border-gray-600 text-white">
                <SelectValue placeholder="Select a discount tier" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-700 text-white">
                <SelectItem value="0">No Discount</SelectItem>
                <SelectItem value="10">10% Off</SelectItem>
                <SelectItem value="20">20% Off</SelectItem>
                <SelectItem value="30">30% Off</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="yearly-billing"
              checked={isYearly}
              onCheckedChange={setIsYearly}
            />
            <Label htmlFor="yearly-billing" className="text-lg">Yearly Billing (Save 10%)</Label>
          </div>
        </div>
        <div className="space-y-6">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2">
            <h3 className="text-xl font-semibold">Pricing Breakdown</h3>
            <ul className="list-disc list-inside space-y-1 text-gray-300">
              <li>Seat Cost: ${(seats * basePrice).toFixed(2)}</li>
              <li>Usage Cost: ${(usage * usageRate).toFixed(2)}</li>
              <li>Discount: {discount}%</li>
              {isYearly && <li>Yearly Discount: 10%</li>}
            </ul>
          </div>
          <motion.div
            className="pt-4"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <h3 className="text-3xl font-bold text-green-400">
              Total {isYearly ? 'Yearly' : 'Monthly'} Price: ${total.toFixed(2)}
            </h3>
          </motion.div>
        </div>
      </CardContent>
    </Card>
  )
}