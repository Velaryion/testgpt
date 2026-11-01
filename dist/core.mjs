export const CATEGORIES = {expense: ['Alimentación', 'Transporte', 'Hogar', 'Ocio', 'Compras', 'Salud', 'Otros'], income: ['Nómina', 'Extra', 'Regalos', 'Otros']};
export function parseAmount(value) {
  const text = String(value).trim().replace(',', '.');
  if (!/^\d+(\.\d{1,2})?$/.test(text)) throw new Error('Introduce un importe con hasta dos decimales.');
  const [whole, decimal = ''] = text.split('.');
  const cents = Number(whole) * 100 + Number(decimal.padEnd(2, '0'));
  if (!Number.isSafeInteger(cents) || cents <= 0 || cents > 10000000000) throw new Error('El importe debe estar entre 0,01 y 100.000.000 €.');
  return cents;
}
export function validDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value + 'T12:00:00Z');
  return Number.isFinite(+date) && date.toISOString().slice(0, 10) === value && value >= '1900-01-01' && value <= '9999-12-31';
}
export function validateEntry(entry) {
  if (!entry || typeof entry !== 'object' || typeof entry.id !== 'string' || !/^[a-zA-Z0-9-]{1,80}$/.test(entry.id) || !['expense', 'income'].includes(entry.type) || !Number.isSafeInteger(entry.amount) || entry.amount <= 0 || entry.amount > 10000000000 || !validDate(entry.date) || !CATEGORIES[entry.type].includes(entry.category) || typeof entry.description !== 'string' || !entry.description.trim() || entry.description.length > 100) throw new Error('Hay un movimiento con datos no válidos.');
  return {id: entry.id, type: entry.type, amount: entry.amount, date: entry.date, category: entry.category, description: entry.description.trim()};
}
export function readBackup(data) {
  if (!data || data.version !== 1 || data.currency !== 'EUR' || !Array.isArray(data.entries) || data.entries.length > 50000) throw new Error('La copia no tiene un formato compatible.');
  const entries = data.entries.map(validateEntry);
  if (new Set(entries.map(e => e.id)).size !== entries.length) throw new Error('La copia contiene identificadores repetidos.');
  return entries;
}
export function summarize(entries) {
  const income = entries.filter(e => e.type === 'income').reduce((sum, e) => sum + e.amount, 0);
  const expense = entries.filter(e => e.type === 'expense').reduce((sum, e) => sum + e.amount, 0);
  return {income, expense, balance: income - expense};
}
