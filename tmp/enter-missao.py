from pathlib import Path
p=Path('mission.js');s=p.read_text(encoding='utf-8');needle=" $('answer-form').addEventListener('submit',check);"
replacement=needle+'''
 // Enter confirms an answer or advances feedback, once per key press.
 document.addEventListener('keydown',event=>{
  if(event.key!=='Enter'||event.isComposing||event.ctrlKey||event.altKey||event.metaKey||event.shiftKey)return;
  const feedback=$('feedback');
  if(document.querySelector('dialog[open]:not(#feedback)'))return;
  if(feedback.open){
   event.preventDefault();
   if(!event.repeat&&!checking&&!$('continue-feedback').disabled)$('continue-feedback').click();
   return;
  }
  if(screen!=='questions')return;
  const control=event.target.closest('button,a,select,textarea,audio,video,summary,[contenteditable="true"]');
  if(control&&control!==$('check-answer'))return;
  event.preventDefault();
  if(event.repeat||checking||$('check-answer').disabled)return;
  $('answer-form').requestSubmit($('check-answer'));
 });
'''
assert needle in s;s=s.replace(needle,replacement);p.write_text(s,encoding='utf-8')
p=Path('mission.html');s=p.read_text(encoding='utf-8').replace('mission.js?v=play-lesson-1','mission.js?v=enter-actions-1');p.write_text(s,encoding='utf-8')
