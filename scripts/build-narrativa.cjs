const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
process.chdir(root);
const ffmpeg = process.env.FFMPEG_PATH || 'C:/Users/USUARIO/Desktop/videos-educacionais/.deps/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';
const texts = JSON.parse(fs.readFileSync('scripts/narrativa-texto.json', 'utf8').replace(/^\uFEFF/, ''));
const out = 'assets/videos/narrativa';
const work = 'tmp/narrativa';
fs.mkdirSync(work, {recursive:true});
fs.mkdirSync(out, {recursive:true});
function run(args) {
  const r = spawnSync(ffmpeg, ['-hide_banner','-loglevel','error','-y',...args], {encoding:'utf8',maxBuffer:8e6});
  if (r.status !== 0) throw new Error(r.stderr || String(r.error));
}
function duration(file) {
  const r = spawnSync(ffmpeg, ['-hide_banner','-i',file], {encoding:'utf8'});
  const m = r.stderr.match(/Duration: (\d+):(\d+):([\d.]+)/);
  if (!m) throw new Error('Duração ausente: '+file);
  return Number(m[1])*3600+Number(m[2])*60+Number(m[3]);
}
function wrap(text, max=73) {
  const lines=[''];
  for(const word of text.split(' ')) {
    if(lines.at(-1).length+word.length+1>max) lines.push(word);
    else lines[lines.length-1]+=(lines.at(-1)?' ':'')+word;
  }
  return lines.join('\n');
}
function stamp(seconds) {
  const ms = Math.round(seconds*1000);
  return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')}.${String(ms%1000).padStart(3,'0')}`;
}
const timeline=[];
let offset=0;
for(const [i,text] of texts.entries()) {
  const id=String(i+1).padStart(2,'0');
  const audio=`assets/sons/narrativa/cena-${id}.mp3`;
  const speech=duration(audio);
  const seconds=Math.ceil((speech+1.1)*30)/30;
  const frames=Math.round(seconds*30);
  const caption=wrap(text);
  fs.writeFileSync(`${work}/texto-${id}.txt`,caption);
  const boxHeight=caption.split('\n').length*39+34;
  const zoom=i%2===0?`1.02+0.075*on/${frames}`:`1.095-0.075*on/${frames}`;
  const x=i%3===0?`(iw-iw/zoom)*(0.3+0.4*on/${frames})`:'(iw-iw/zoom)/2';
  const filters=[
    'scale=2560:1440:force_original_aspect_ratio=increase','crop=2560:1440',
    `zoompan=z='${zoom}':x='${x}':y='(ih-ih/zoom)/2':d=${frames}:s=1280x720:fps=30`,
    'setsar=1',
    `drawbox=x=0:y=${720-boxHeight}:w=iw:h=${boxHeight}:color=0x101E3B@0.86:t=fill`,
    `drawbox=x=48:y=${720-boxHeight}:w=1184:h=3:color=0xA0006D@0.95:t=fill`,
    `drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':textfile='${work}/texto-${id}.txt':fontcolor=0xEFFAFD:fontsize=31:line_spacing=8:x=(w-text_w)/2:y=${720-boxHeight+17}`,
    ...Array.from({length:8},(_,j)=>`drawbox=x=${48+j*21}:y=30:w=12:h=4:color=${j===i?'0xFFD166':'0xEFFAFD@0.4'}:t=fill`),
    'fade=t=in:st=0:d=0.35',`fade=t=out:st=${seconds-0.35}:d=0.35`,'format=yuv420p'
  ];
  const segment=`${work}/cena-${id}.mp4`;
  run(['-i',`assets/imagens/narrativa/cena-${id}.png`,'-i',audio,'-vf',filters.join(','),'-af',`adelay=400|400,apad,loudnorm=I=-16:TP=-1.5:LRA=11`,'-t',String(seconds),'-c:v','libx264','-preset','fast','-crf','20','-threads','4','-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',segment]);
  timeline.push({scene:i+1,text,start:offset,end:offset+seconds,speechStart:offset+0.4,speechEnd:offset+0.4+speech});
  offset+=seconds;
  console.log(`Cena ${id} renderizada: ${seconds.toFixed(2)} s`,true);
}
fs.writeFileSync(`${work}/concat.txt`,timeline.map(t=>`file 'cena-${String(t.scene).padStart(2,'0')}.mp4'`).join('\n'));
run(['-f','concat','-safe','0','-i',`${work}/concat.txt`,'-c','copy','-movflags','+faststart',`${out}/orbita-a-missao.mp4`]);
fs.writeFileSync(`${out}/narrativa.vtt`,'WEBVTT\n\n'+timeline.map(t=>`${t.scene}\n${stamp(t.start+0.35)} --> ${stamp(t.end-0.25)}\n${t.text}\n`).join('\n'));
fs.writeFileSync(`${out}/timeline.json`,JSON.stringify({voice:'pt-BR-FranciscaNeural',duration:offset,scenes:timeline},null,2));
run(['-ss',String(timeline[2].start+2),'-i',`${out}/orbita-a-missao.mp4`,'-frames:v','1','-q:v','2',`${out}/poster.jpg`]);
console.log(`Vídeo pronto: ${offset.toFixed(2)} s, ${Math.round(fs.statSync(`${out}/orbita-a-missao.mp4`).size/1e6)} MB`);
