import test from 'node:test';
import assert from 'node:assert/strict';
import {parseAmount, validDate, readBackup, summarize} from '../dist/core.mjs';
const entry={id:'test-1',type:'expense',amount:1234,date:'2026-11-01',category:'Alimentación',description:'Supermercado'};
test('importes monetarios exactos en céntimos, con coma o punto',()=>{assert.equal(parseAmount('12,34'),1234);assert.equal(parseAmount('0.01'),1);assert.equal(parseAmount('20'),2000);for(const amount of ['0','-1','NaN','1e3','1.999','1.000,00','9007199254740993'])assert.throws(()=>parseAmount(amount));});
test('fechas reales y años bisiestos',()=>{assert.ok(validDate('2024-02-29'));for(const date of ['2026-02-29','2026-02-30','2026-13-01','01/11/2026','1899-12-31'])assert.equal(validDate(date),false);});
test('balance mantiene céntimos y diferencia ingresos de gastos',()=>{assert.deepEqual(summarize([entry,{...entry,id:'test-2',type:'income',amount:200000,category:'Nómina'}]),{income:200000,expense:1234,balance:198766});assert.deepEqual(summarize([]),{income:0,expense:0,balance:0});});
test('copias válidas se restauran sin campos ajenos',()=>{assert.deepEqual(readBackup({version:1,currency:'EUR',entries:[{...entry,unknown:'x'}]}),[entry]);});
test('copias incompatibles o dañadas se rechazan antes de escribir',()=>{for(const data of [null,{version:2,currency:'EUR',entries:[]},{version:1,currency:'USD',entries:[]},{version:1,currency:'EUR',entries:[entry,entry]},...['amount','date','type','category','id','description'].map(key=>({version:1,currency:'EUR',entries:[{...entry,[key]:null}]}))])assert.throws(()=>readBackup(data));});
