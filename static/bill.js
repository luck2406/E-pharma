let discountMoney = 0;
takenMedicines = {};
let nextMedNo = 0;

const GenerateBill = () => {
  let patient = document.getElementById("pName").value;
  let doctor = document.getElementById("Dname").value;
  let total = document.getElementById("total").innerHTML;
  let subtotal = document.getElementById("subtotal").innerHTML;
  let discount = document.getElementById("discounted").value;
  if (patient == "" || doctor == "") {
    alert("Please fill all the fields");
    return;
  }
  if (total == 0) {
    alert("Please add some medicines");
    return;
  }
  if (discount == "") {
    discount = 0;
  }
  let medicines = takenMedicines;
  let data = {
    patient,
    doctor,
    total,
    subtotal,
    discount,
    medicines,
  };
  fetch("/api/bill", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.status == "success") {
        window.location.href = "/bill/" + data.billId;
      }
      if (data.status == "StockOut") {
        alert(
          `Item ${data.med} is not sufficient in stock\nPlease reduce the quantity\nCurrent stock is ${data.stock}`
        );
      }
    });
};

const syncTotal = () => {
  let ttl =
    Number(document.getElementById("subtotal").innerHTML) -
    Number(document.getElementById("discounted").value);
  if (ttl < 0) {
    ttl = 0;
  }
  document.getElementById("total").innerHTML = Math.ceil(ttl);
};

const NewDiscount = () => {
  let newDiscount = document.getElementById("discounted").value;
  let newprice =
    Number(document.getElementById("subtotal").innerHTML) - Number(newDiscount);
  // console.log("Discounted price: ",newprice, "Discount: ",newDiscount , Number(document.getElementById("subtotal").innerHTML));
  if (newprice <= 0) {
    alert("Discount is too high");
    return;
  }
  discountMoney = newDiscount;
  //   document.getElementById("total").innerText = newprice;
  syncTotal();
};

const DiscountedPrice = () => {
  let discount = document.getElementById("discount").value;
  let total = document.getElementById("subtotal").innerHTML;
  let discounted = Math.round(((total * discount) / 100) * 100) / 100;
  discountMoney = discounted;
  document.getElementById("discounted").value = discounted;
  document.getElementById("total").innerHTML = Math.ceil(total - discounted);
};

const getPrice = async (medicine) => {
  const response = await fetch(`/api/medicine/${medicine}`);
  const data = await response.json();
  console.log(data.price);
  return data;
};
const changequantity = (tab, medNo) => {
  console.log(medNo, tab);
  med = takenMedicines[medNo].medicine;
  const medqty = document.getElementById(med).value;
  console.log(medqty, medNo);
  let oldqty = takenMedicines[medNo].quantity;
  const medprice = document.getElementById(`row-${medNo}`).childNodes[2]
    .innerHTML;
  console.log(medprice);
  const total = medprice * medqty;
  document.getElementById(`row-${medNo}`).childNodes[3].innerHTML =
    Math.round(total * 100) / 100;
  takenMedicines[medNo].quantity = medqty;
  console.log(takenMedicines);
  let subt = document.getElementById("subtotal").innerHTML;
  subt = Number(subt) - Math.round(oldqty * medprice * 100) / 100;
  subt = Number(subt) + Math.round(medqty * medprice * 100) / 100;
  document.getElementById("subtotal").innerHTML = subt;
  syncTotal();
};

const removeRow = (rowid) => {
  console.log(rowid);
  let qty = takenMedicines[rowid].quantity;
  const medprice = document.getElementById(`row-${rowid}`).childNodes[2]
    .innerHTML;
  let subt = document.getElementById("subtotal").innerHTML;
  subt = Number(subt) - qty * medprice;
  document.getElementById("subtotal").innerHTML = subt;
  syncTotal();
  document.getElementById(`row-${rowid}`).remove();
  delete takenMedicines[rowid];
  console.log(takenMedicines);
};

const selectThis = async () => {
  let medicine = document.getElementById("medicine").value;
  let quantity = document.getElementById("medicine").nextElementSibling.value;

  if (quantity == "0" || quantity == 0) {
    alert("Select Quantity");
    return;
  }
  const response = await fetch(`/api/medicine/${medicine}`);
  const data = await response.json();
  let price = data.price;
  let qty = data.quantity;
  if (quantity > qty) {
    alert(
      `${medicine} is not sufficient in stock\nPlease reduce the quantity\nCurrent stock is ${qty}`
    );
    let quantity = (document.getElementById(
      "medicine"
    ).nextElementSibling.value = 0);
    return;
  }
  console.log(price);
  let table = document.getElementsByTagName("table")[0];
  let row = table.insertRow(1);
  let cell1 = row.insertCell(0);
  let cell2 = row.insertCell(1);
  let cell3 = row.insertCell(2);
  let cell4 = row.insertCell(3);
  let cell5 = row.insertCell(4);

  x = document.createElement("input");
  x.setAttribute("type", "number");
  x.setAttribute("id", medicine);
  x.setAttribute("min", "0");
  x.setAttribute("class", "inpchange");
  x.setAttribute("onchange", `changequantity(${quantity},${nextMedNo})`);
  x.setAttribute("value", quantity);

  clse = document.createElement("img");
  clse.setAttribute("src", "/static/close.svg");
  clse.setAttribute("onclick", `removeRow(${nextMedNo})`);
  clse.setAttribute("class", "close");

  cell1.innerHTML = medicine;
  cell2.appendChild(x);
  cell3.innerHTML = price;
  cell4.innerHTML = Math.round(price * quantity * 100) / 100;
  cell5.appendChild(clse);
  document.getElementById("medicine").value = "";
  document.getElementById("medicine").nextElementSibling.value = "0";
  document.getElementById("altbtn").style.display = "none";
  document.getElementById("alternatives").innerHTML = "";
  row.setAttribute("id", `row-${nextMedNo}`);
  let old = document.getElementById("subtotal").innerHTML;
  // console
  document.getElementById("subtotal").innerHTML =
    Math.round(Number(price * quantity) * 100) / 100 + Number(old);
  syncTotal();
  takenMedicines[nextMedNo++] = {
    medicine: medicine,
    quantity: quantity,
  };
};

$(function () {
  $("#medicine").autocomplete({
    delay: 300,
    source: function (request, response) {
      var medSearch = request.term;
      var meds = [];
      $.ajax({
        url: "/findMedicine",
        data: {
          med: medSearch,
        },
        method: "POST",
        headers: {
          "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
            .value,
        },
        success: function (data) {
          $.each(data, function (key, value) {
            console.log(value);
            meds.push(value);
          });
          response(meds);
          if (meds.length == 0) {
            document.getElementById("altbtn").style.display = "block";
            console.log(meds);
          }
          if (meds.length != 0) {
            document.getElementById("altbtn").style.display = "none";
            // console.log("--", meds[0]);
          }
        },
      });
    },
  });
});

const choosethis = (medName) => {
  console.log(medName);
  document.getElementById("medicine").value = medName;
};

const showAlternative = (data) => {
  $("#alternatives").html("");
  $.each(data, function (key, value) {
    console.log(value);
    if (key == "FetchedComp") {
      alert(`Found with differnt Mg: ${value[0]}\nIn store:  ${value[1]}`);
      return;
    }
    $("#alternatives").append(
      `<div class="showalts"><strong>${key}</strong> - price: ${value[1]} Quantity: ${value[0]} <span onclick="choosethis('${key}')"><img src = "/static/check.png" height="30px"></span></div>`
    );
  });
};

function findALternative() {
  var med = document.getElementById("medicine").value;
  $.ajax({
    url: "/findAlternative",
    data: {
      med: med,
    },
    method: "POST",
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
    },
    success: function (data) {
      showAlternative(data);
      console.log("--",data.keys, data.values, data);
      t = JSON.stringify(data);
      console.log("-----", t.length);
      if (t.length == 2) {
        alert("Not Found");
        return;
      }
    },
  });
}

$("#mednums").on("keypress", function (e) {
  if (e.which == 13) {
    selectThis();
  }
});

$(function () {
  $("#Composition_search").autocomplete({
    delay: 300,
    source: function (request, response) {
      var medSearch = request.term;
      var meds = [];
      $.ajax({
        url: "/findMedicineByComposition",
        data: {
          comp: medSearch,
        },
        method: "POST",
        headers: {
          "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
            .value,
        },
        success: function (data) {
          $.each(data, function (key, value) {
            console.log("*****",value);
            meds.push(value);
          });
          response(meds);
          console.log(meds);
          if (meds.length == 0) {
            document.getElementById("altbtn").style.display = "block";
            console.log(meds);
          }
          if (meds.length != 0) {
            document.getElementById("altbtn").style.display = "none";
            console.log("--", meds);
          }
        },
      });
    },
  });
});
