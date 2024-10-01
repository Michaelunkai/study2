document.addEventListener("DOMContentLoaded", function() {
    const calendarBody = document.getElementById("calendarBody");
    const currentMonthDisplay = document.getElementById("currentMonth");
    const prevMonthBtn = document.getElementById("prevMonthBtn");
    const nextMonthBtn = document.getElementById("nextMonthBtn");
  
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();
  
    renderCalendar(currentMonth, currentYear);
  
    prevMonthBtn.addEventListener("click", () => {
      currentYear = currentMonth === 0 ? currentYear - 1 : currentYear;
      currentMonth = currentMonth === 0 ? 11 : currentMonth - 1;
      renderCalendar(currentMonth, currentYear);
    });
  
    nextMonthBtn.addEventListener("click", () => {
      currentYear = currentMonth === 11 ? currentYear + 1 : currentYear;
      currentMonth = currentMonth === 11 ? 0 : currentMonth + 1;
      renderCalendar(currentMonth, currentYear);
    });
  
    function renderCalendar(month, year) {
      calendarBody.innerHTML = "";
      const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      currentMonthDisplay.textContent = `${monthNames[month]} ${year}`;
  
      const firstDayOfMonth = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
  
      for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyDay = document.createElement("div");
        emptyDay.classList.add("calendar-day");
        calendarBody.appendChild(emptyDay);
      }
  
      for (let i = 1; i <= daysInMonth; i++) {
        const calendarDay = document.createElement("div");
        calendarDay.textContent = i;
        calendarDay.classList.add("calendar-day");
        if (year === currentDate.getFullYear() && month === currentDate.getMonth() && i === currentDate.getDate()) {
          calendarDay.classList.add("today");
        }
        calendarBody.appendChild(calendarDay);
      }
    }
  });
  