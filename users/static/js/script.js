async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        alert(error);
    }
}

async function fetchDataNoReload(event, url, options = {}) {
  event.preventDefault();
  try {
      const response = await fetch(url, options);
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
  } catch (error) {
      console.error('Fetch error:', error);
      alert(error);
  }
}

async function deletionAPI(url, options = {}){
  try{
    const response = await fetch(url, options);
    if(!response.ok){
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response;
  } catch(error) {
    console.error('Fetch error:', error);
    alert(error);
  }
}

function displayStudentsInClass(result, counter){
  const studentList = document.getElementById('studentList');
  const classDetailModal = document.getElementById('classDetailModal');
  const enrollmentInput = document.getElementById('enrollInput');
  enrollInput.value="";

  for (i = 0; i < result.length; i++) {

    classDetailModal.textContent = result[i].course_title;

    if(result[i].enrollmentList){
      enrollmentList = result[i].enrollmentList;

      for (j = 0; j < enrollmentList.length; j++){
        const studentListRow = document.createElement('div');
        const p = document.createElement('p');
        const removeButton = document.createElement('a');
        p.textContent = `${enrollmentList[j].student_name} ${enrollmentList[j].phone_num}`;
        removeButton.textContent = "Remove";
        removeButton.setAttribute("onclick", `deleteEnrollment(${enrollmentList[i].enrollment_pk})`);
        removeButton.setAttribute("class", "deleteURL");
        removeButton.setAttribute("type", "button");
        p.setAttribute("class", "studentListItem");
        studentListRow.setAttribute("class", "studentListRow");
        studentListRow.append(p);
        studentListRow.append(removeButton);
        if(!studentList.textContent.includes(p.textContent)){
          studentList.append(studentListRow);
        }
      }
    }
  }
}

function enrollmentAction(event){
  event.preventDefault();
  url = "/timetable/";
  options = {
    method: "POST",
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      'phoneNum': enrollInput.value,
      'classID': courseID
    }),
    credentials: 'same-origin'
  }
  fetchDataNoReload(event, url, options).then(result => {
    alert(result['enroll_response']);
    enrollInput.value = "";
  })
}

function deleteClass(courseID){
  const DeleteClassButton = document.getElementById('DeleteClassButton');
  DeleteClassButton.addEventListener("click", ()=>{
    var confirmDelete = confirm("Are you sure you want to delete this class?");
    url = `/delete-class/${courseID}`;
    options = {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        "classID": courseID,
      })
    }

    if(confirmDelete){
      deletionAPI(url, options).then(
        result=>{
          location.reload();
        }
      );
    }else{
      return;
    }
  });
}

function deleteEnrollment(enrollmentID){
  var confirmDelete = confirm("Are you sure you want to remove this student from this class?");

  if(confirmDelete){
    url = `/enrollment/delete/${enrollmentID}`;
    options = {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      }
    }
    deletionAPI(url, options).then(
      result=>{
        location.reload();
      }
    );
  }else{
    return;
  }
}
