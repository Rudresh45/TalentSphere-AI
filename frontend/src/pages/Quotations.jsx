import React, { useState } from 'react';
import { FileText, Plus, Calculator, CheckCircle2 } from 'lucide-react';

const mockProducts = [
  { id: 1, name: 'TalentSphere Enterprise License', price: 4999.00, tax: 18.0 },
  { id: 2, name: 'AI Skill Gap Analytics Addon', price: 1499.00, tax: 18.0 },
  { id: 3, name: 'Custom ERP Integration Module', price: 2999.00, tax: 18.0 },
  { id: 4, name: 'Dedicated Cloud Hosting (Monthly)', price: 899.00, tax: 18.0 },
];

const Quotations = () => {
  const [selectedProduct, setSelectedProduct] = useState(mockProducts[0]);
  const [quantity, setQuantity] = useState(2);
  const [discountPercent, setDiscountPercent] = useState(10);

  // Live Calculations
  const subtotal = selectedProduct.price * quantity;
  const discountAmount = subtotal * (discountPercent / 100);
  const taxableAmount = subtotal - discountAmount;
  const taxAmount = taxableAmount * (selectedProduct.tax / 100);
  const grandTotal = taxableAmount + taxAmount;

  return (
    <div className="space-y-8">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Quotation & Pricing Engine</h2>
          <p className="text-xs text-slate-400 mt-1">Generate customer quotes with dynamic discount rules, automated tax calculation, and approval workflows.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Interactive Quote Builder */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 lg:col-span-2 space-y-5">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Calculator className="w-4 h-4 text-cyan-400" />
            <span>Interactive Quotation Generator</span>
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1">Select Product / Module</label>
              <select
                value={selectedProduct.id}
                onChange={(e) => setSelectedProduct(mockProducts.find(p => p.id === parseInt(e.target.value)))}
                className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                {mockProducts.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} — ${p.price.toFixed(2)} (Tax: {p.tax}%)
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Quantity</label>
                <input
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                  className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Discount (%)</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={discountPercent}
                  onChange={(e) => setDiscountPercent(Math.min(100, Math.max(0, parseFloat(e.target.value) || 0)))}
                  className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Live Invoice Preview */}
        <div className="glass-panel p-6 rounded-3xl border border-blue-500/30 bg-blue-950/10 space-y-4">
          <h3 className="text-base font-bold text-white border-b border-slate-800 pb-3">Price Breakdown Summary</h3>

          <div className="space-y-3 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-400">Unit Price:</span>
              <span className="text-slate-200">${selectedProduct.price.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Quantity:</span>
              <span className="text-slate-200">x{quantity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Gross Subtotal:</span>
              <span className="text-slate-200">${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-rose-400">
              <span>Discount ({discountPercent}%):</span>
              <span>-${discountAmount.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-cyan-400">
              <span>Tax ({selectedProduct.tax}%):</span>
              <span>+${taxAmount.toFixed(2)}</span>
            </div>
            <div className="flex justify-between border-t border-slate-800 pt-3 text-sm font-sans font-bold">
              <span className="text-white">GRAND TOTAL:</span>
              <span className="text-emerald-400 text-lg">${grandTotal.toFixed(2)}</span>
            </div>
          </div>

          <button className="w-full glass-button py-3 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 cursor-pointer mt-4">
            <CheckCircle2 className="w-4 h-4" />
            <span>Generate Official Quotation</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Quotations;
