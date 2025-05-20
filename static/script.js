document.addEventListener("DOMContentLoaded", function () {
  const expenses = window.expensesData;

  // Fill summary
  const total = expenses.reduce((acc, e) => acc + parseFloat(e.amount), 0);
  document.getElementById("summary").textContent = `Total: $${total.toFixed(2)}`;

  // Bar Chart by Category
  const categoryMap = {};
  expenses.forEach(e => {
    categoryMap[e.category] = (categoryMap[e.category] || 0) + parseFloat(e.amount);
  });

  const categories = Object.keys(categoryMap);
  const amounts = Object.values(categoryMap);

  const ctx = document.getElementById("expenseChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: categories,
      datasets: [{
        label: "Expenses by Category",
        data: amounts,
        backgroundColor: "rgba(75, 192, 192, 0.7)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: "Expense Breakdown"
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Theme toggle
  const themeBtn = document.getElementById("themeToggle");
  themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });
});
