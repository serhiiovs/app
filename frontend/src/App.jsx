import { useState } from "react";

function App() {
  const [date, setDate] = useState("");
  const [rates, setRates] = useState(null);

  const fetchRates = async () => {
    const res = await fetch(`/api/rates?day=${date}`);
    const data = await res.json();
    setRates(data.rates);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>USD Exchange Rates</h1>

      <input
        type="date"
        value={date}
        onChange={e => setDate(e.target.value)}
      />
      <button onClick={fetchRates}>Load</button>

      {rates && (
        <table border="1" cellPadding="4">
          <thead>
            <tr>
              <th>Currency</th>
              <th>Rate</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(rates).map(([c, r]) => (
              <tr key={c}>
                <td>{c}</td>
                <td>{r}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
