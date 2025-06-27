import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

function App() {
  const [data, setData] = useState([]);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/filters").then((res) => {
      setTopics(res.data.topics.filter(Boolean));
    });
  }, []);

  useEffect(() => {
    let url = "http://localhost:8000/data";
    if (selectedTopic) {
      url = `http://localhost:8000/filtered-data?topic=${selectedTopic}`;
    }
    axios.get(url).then((res) => {
      setData(res.data);
    });
  }, [selectedTopic]);

  const chartData = {
    labels: data.map((item) => item.title),
    datasets: [
      {
        label: "Intensity",
        data: data.map((item) => item.intensity),
        backgroundColor: "rgba(75,192,192,0.6)"
      }
    ]
  };

  return (
    <div>
      <h2>Blackcoffer Dashboard</h2>
      <select onChange={(e) => setSelectedTopic(e.target.value)}>
        <option value="">All Topics</option>
        {topics.map((topic, idx) => (
          <option key={idx} value={topic}>{topic}</option>
        ))}
      </select>
      <Bar data={chartData} />
    </div>
  );
}

export default App;
