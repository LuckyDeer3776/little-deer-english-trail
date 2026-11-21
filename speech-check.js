(function(root){
  'use strict';
  const numbers='zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(' ');
  const contractions={"it's":'it is',"i'm":'i am',"you're":'you are',"we're":'we are',"they're":'they are',"he's":'he is',"she's":'she is',"that's":'that is',"there's":'there is',"don't":'do not',"doesn't":'does not',"didn't":'did not',"can't":'can not',"won't":'will not',"isn't":'is not',"aren't":'are not',"i've":'i have',"i'll":'i will',"let's":'let us'};
  function tokens(text){return String(text||'').replace(/[’‘]/g,"'").match(/[A-Za-z0-9]+(?:'[A-Za-z]+)*/g)||[]}
  function expand(word){const lower=word.toLowerCase();return (Object.prototype.hasOwnProperty.call(contractions,lower)?contractions[lower]:lower).split(' ').map(w=>/^\d+$/.test(w)&&Number(w)<=20?numbers[Number(w)]:w)}
  function words(text){return tokens(text).flatMap(expand)}
  function compare(target,heard){
    const original=tokens(target),a=original.flatMap((word,index)=>expand(word).map(value=>({value,index}))),b=words(heard);
    const dp=Array.from({length:a.length+1},()=>new Uint32Array(b.length+1));
    for(let i=a.length-1;i>=0;i--)for(let j=b.length-1;j>=0;j--)dp[i][j]=a[i].value===b[j]?1+dp[i+1][j+1]:Math.max(dp[i+1][j],dp[i][j+1]);
    const hits=original.map(()=>0),extra=[];let i=0,j=0;
    while(i<a.length&&j<b.length){if(a[i].value===b[j]){hits[a[i].index]++;i++;j++}else if(dp[i+1][j]>=dp[i][j+1])i++;else extra.push(b[j++])}
    while(j<b.length)extra.push(b[j++]);
    const items=original.map((word,index)=>({word,status:hits[index]===expand(word).length?'ok':'missed'}));
    return {items,extra,matched:items.filter(item=>item.status==='ok').length,total:items.length};
  }
  const api={words,compare};if(typeof window!=='undefined')window.SpeechCheck=api;if(typeof module!=='undefined')module.exports=api;
})(this);
