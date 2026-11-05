(() => {
 'use strict';
 const missions=[window.ORBITA_MISSION,window.ORBITA_MISSION_2];
 const requested=Number(new URLSearchParams(window.location.search).get('mission'));
 window.ORBITA_MISSIONS=missions;
 window.ORBITA_MISSION=missions.find(m=>m.id===requested)||missions[0];
 document.title=`Órbita 2 • ${window.ORBITA_MISSION.title}`;
})();
