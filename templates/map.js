// const iconData = {
//   cafe: "image/geo-cafe.svg",
//   museum: "image/geo-muzei.svg",
//   attractions: "image/geo-dostoprim.svg",
// }
window.onresize = function (){
  if (window.outerWidth < 428 || window.outerHeight < 926){
      window.resizeTo(428, 926);
  }
  else if (window.outerWidth > 428 || window.outerHeight > 926){
      window.resizeTo(428, 926);
  }
}



const init = () => {
  const map = new ymaps.Map('mapContainer', {
    center: [61.25454375819568, 73.39883882118488],
    zoom: 14,
  });
  map.controls.remove('geolocationControl'); // удаляем геолокацию
  map.controls.remove('searchControl'); // удаляем поиск
  map.controls.remove('trafficControl'); // удаляем контроль трафика
  map.controls.remove('typeSelector'); // удаляем тип
  map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
  map.controls.remove('zoomControl'); // удаляем контрол зуммирования
  map.controls.remove('rulerControl'); // удаляем контрол правил
  
  test(map);
}

async function test(map)
{
  let arr = await eel.getMap()();
  for(let i = 0; i < arr.length; i++){
    const placemark = new ymaps.Placemark([arr[i][2], arr[i][3]], {
      hintContent: arr[i][0],
      balloonContent: arr[i][1],
    }, {});
    
    map.geoObjects.add(placemark);
  }
}

document.addEventListener("DOMContentLoaded", function(){
  ymaps.ready(init);
});

