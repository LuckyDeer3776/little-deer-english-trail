'use strict';
const assert=require('node:assert/strict');
const {words,compare}=require('../speech-check.js');
const cases=[
  ['perfect match',()=>assert.deepEqual(compare('We like apples','We like apples'),{items:[{word:'We',status:'ok'},{word:'like',status:'ok'},{word:'apples',status:'ok'}],extra:[],matched:3,total:3})],
  ['missed words',()=>assert.deepEqual(compare('We really like red apples','We like apples').items.filter(x=>x.status==='missed').map(x=>x.word),['really','red'])],
  ['extra words',()=>assert.deepEqual(compare('We like apples','We really like green apples').extra,['really','green'])],
  ['punctuation and case',()=>assert.equal(compare('Hello, WORLD!','hello world.').matched,2)],
  ['number equivalence',()=>assert.equal(compare('I have 9 pens and twenty books','I have nine pens and 20 books').matched,7)],
  ['contractions',()=>{assert.equal(compare('It’s fine, I am ready',"it is fine i'm ready").matched,5);assert.equal(compare('it is fine',"it's fine").matched,3)}],
  ['empty input',()=>{assert.deepEqual(compare('',''),{items:[],extra:[],matched:0,total:0});assert.equal(compare('Hello','').items[0].status,'missed');assert.deepEqual(compare('','hello').extra,['hello'])}],
  ['missing input',()=>assert.deepEqual(words(null),[])],
  ['repeated word alignment',()=>assert.equal(compare('go go home','go home').matched,2)]
];
for(const [name,test] of cases){test();console.log('PASS '+name)}
console.log('All '+cases.length+' speech-check tests passed.');
