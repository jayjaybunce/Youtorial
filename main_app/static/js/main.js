



let titleInputEl = document.querySelector('#id_title')
let titleEl = document.querySelector('#tutorial_title')
if(document.querySelector('#id_title')){
  titleInputEl.addEventListener('input',handleTitleChange)
}

if(document.querySelector('#id_video')){
  console.log('setting up listener')
  let fileEl = document.querySelector('#id_video')
  fileEl.addEventListener('click',handlFileClick)
}


function handlFileClick(evt){
  let videoInputEl = document.querySelector('#id_video_url')
  videoInputEl.value = ''


}






// if(document.querySelector('#id_content')){
//   window.addEventListener('beforeunload', (event) => {
//     event.returnValue = `Are you sure you want to leave?`;
//   });
// }

function handleTitleChange(evt){
  let val = titleInputEl.value
  titleEl.textContent = val




}