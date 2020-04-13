import React from 'react';
import './App.css';
import axios from 'axios';
import {Line} from 'react-chartjs-2';


class LinePlot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: {
        labels: ['1', '2', '3', '4', '5'],
        datasets: []
      },
    }
  }

  componentDidMount() {
    this.getData();
  }

  getData() {
    axios
      .get('http://localhost:8888/results/separation/tau/3')
      .then(response => {
        this.setState(prevState => ({
          data: {
            ...prevState.data,
            datasets: Object.entries(response.data).map(([key, value]) => {
              return {
                label: key,
                fill: false,
                data: Object.keys(value).map((key, index) => value[key])
              }
            })
          }
        }));
        this.setState({loading: false});
      })
      .catch(error => console.log(error.response));
  }

  render() {
    return (
      <div>
        {this.state.loading ? <b>Loading...</b> : <Line data={this.state.data} />}
      </div>
    );
  }
}

class ExperimentSelector extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      schemas: [],
      selected: 'default'
    };

    this.onSelect = this.onSelect.bind(this);
  }

  componentDidMount() {
    axios
      .get('http://localhost:8888/experiments')
      .then(response => {
        this.setState({
          schemas: response.data
        });
      })
      .catch(error => console.log(error.response));
  }

  onSelect (e) {
    this.setState({selected: e.target.value});
  }

  render() {
    return (
        <select id="experiment" onChange={this.onSelect}>
          {
            this.state.schemas.map((item, i) => {
              return (
                <option value={item} key={i}>{ item }</option>
              )
            })
          }
        </select>
    );
  }
}

function App() {
  return (
    <div className="App">
      <ExperimentSelector />

      <div className="container">
        <LinePlot />
      </div>
    </div>
  );
}

export default App;
