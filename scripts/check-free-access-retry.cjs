const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
async function scenario(review,secondCorrect){
 const elements=new Map();let selected=0;
 const el=id=>{if(!elements.has(id))elements.set(id,{value:'',options:[],dataset:{},classList:{toggle(){}},addEventListener(){},pause(){},close(){},showModal(){},focus(){},querySelector(){return null},append(){},click(){this.onclick()},textContent:''});return elements.get(id)};
 const context={window:{addEventListener(){},OrbitaRewards:{daily(){return {}}},OrbitaWallet:{async grant(){}}},document:{getElementById:el,body:{dataset:{}},addEventListener(){},querySelector(){return {value:String(selected)}}},localStorage:{getItem(){return JSON.stringify({done:review?['d1-q1']:[],attempted:review?['d1-q1']:[],attempts:{},errors:{}})},setItem(){}},console};
 vm.createContext(context);vm.runInContext(fs.readFileSync('mission-data.js','utf8'),context);
 const code=fs.readFileSync('mission.js','utf8').replace(' voices();trail();',' window.test={question,check,index:()=>qi};');vm.runInContext(code,context);
 context.window.test.question();await context.window.test.check({preventDefault(){}});
 assert.equal(el('continue-feedback').textContent,'Tentar mais uma vez');el('continue-feedback').click();assert.equal(context.window.test.index(),0);
 selected=secondCorrect?1:0;await context.window.test.check({preventDefault(){}});assert.equal(el('continue-feedback').textContent,'Continuar');el('continue-feedback').click();assert.equal(context.window.test.index(),1);
}
(async()=>{for(const review of [false,true])for(const correct of [false,true])await scenario(review,correct);console.log('OK: primeira resposta errada mantém a questão; segunda resposta avança, com acerto ou erro, em questões novas e já respondidas.');})().catch(e=>{console.error(e);process.exitCode=1});
