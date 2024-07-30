import React, {useState} from "react";
import Select from "react-select";
import "./App.css";
import Loader from "./components/Loader";

import axios from "axios";

const options = [
  { value: "events_info", label: "Events Information" },
  { value: "people_info", label: "People Information" },
  { value: "company_info", label: "Company Information" },
];

function App() {
  const [datab̥ase,setDatabase] = useState("");
  const [query,setQuery] = useState("");
  const [result,setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [valid,setValid] = useState({
    db:false,
    query:false
  });
  const [copied,setCopied] = useState(false);
  const getDB =(selected) =>{
    /**
    selected= {
    value = 'company Information',
    label = 'company Information'
    }
    **/
    setDatabase(selected);
    setValid({db:true,query:valid.query});
    setCopied(false);
  }

  const getQuery =(event) => {
    setQuery(event.target.value);
    setValid({db:valid.db,query:event.target.value.length === 0 ? false :true,});
    setCopied(false);
  };
  console.log(valid);
  const generateQuery = async () =>{
    let finalQuery = `create a SQL request to
     ${query.charAt(0).toLocaleLowerCase()+query.slice(1)} for table ${datab̥ase.value} `;
    console.log(finalQuery);
    setLoading(true);
    //api call for final table reponse
    // const response = "data for the final table response"
    const fetchData = () => {
      axios
        .get("http://127.0.0.1:6000/" + query)
        .then((res) => {
          console.log(res);
          setLoading(false);
          setResult(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    
  }
  return (
    <div className="App">
      <h1 className="heading-top">Database Query Generator!</h1>
      <div className="app-inner">
        <Select
          placeholder="Select Your Table.."
          options={options}
          className="react-select"
          onChange={getDB}
        />

        <textarea
          rows={4}
          className="query-input"
          onChange={getQuery}
          placeholder={`Enter your Database Query. \n\nFor Example, find all users who live in California and have over 1000 credits..`}
        />

        <button disabled={valid.db && valid.query ? false:true} onClick={generateQuery} className="generate-query">
          Generate Query
        </button>
        {!loading? (
          result.length > 0 ?
          <div className="result-text">
          <button onClick ={() => {
            navigator.clipboard.writeText(result);
            setCopied(true);
          }}
          className="copy-btn">{copied? 'Copied':'Copy'}</button>
          <h3 className="result-table">
            {result}
          </h3>
        </div> : <></>
        
        ):(
          <Loader/>
        )}

      </div>
    </div>
  );
}

export default App;