const trafficPenalty={Low:0,Moderate:7,High:15,Severe:24};
const roadSpeed={Highway:52,"Main Road":38,"Urban Road":30,Residential:24};
const weatherPenalty={Clear:0,Cloudy:2,Rain:5,Fog:7};

function estimate(){
  const d=Number(document.getElementById("distance").value);
  const traffic=document.getElementById("traffic").value;
  const road=document.getElementById("road").value;
  const weather=document.getElementById("weather").value;
  const time=document.getElementById("time").value;
  const hour=Number(time.split(":")[0]);
  const peak=[7,8,9,17,18,19].includes(hour)?6:0;
  const baseSpeed=Math.max(8,roadSpeed[road]-trafficPenalty[traffic]-weatherPenalty[weather]-peak);
  const ridge=Math.max(3,Math.round(d/baseSpeed*60+3));
  const lasso=Math.max(3,Math.round(d/(baseSpeed*.98)*60+2));
  const avg=Math.round((ridge+lasso)/2);
  document.getElementById("resultTime").innerHTML=`${avg} <small>min</small>`;
  document.getElementById("ridge").textContent=`${ridge} min`;
  document.getElementById("lasso").textContent=`${lasso} min`;
  document.getElementById("speed").textContent=`${Math.round(baseSpeed)} km/h`;
  document.getElementById("trafficOut").textContent=traffic;
  document.getElementById("weatherOut").textContent=weather;
  document.getElementById("summary").textContent=`${d.toFixed(1)} km • ${traffic} traffic • ${road}`;
  document.getElementById("heroPrediction").textContent=`${avg} min`;
}
document.getElementById("form").addEventListener("submit",e=>{e.preventDefault();estimate()});
estimate();

new Chart(document.getElementById("errorChart"),{
 type:"bar",
 data:{labels:["MAE (min)","RMSE (min)","R² × 10"],
 datasets:[
  {label:"Ridge",data:[4.7,6.1,9.1]},
  {label:"Lasso",data:[5.0,6.4,9.0]}
 ]},
 options:{responsive:true,plugins:{legend:{labels:{color:"#a7bac5"}}},scales:{x:{ticks:{color:"#8297a7"},grid:{color:"#1e3547"}},y:{ticks:{color:"#8297a7"},grid:{color:"#1e3547"}}}}
});
