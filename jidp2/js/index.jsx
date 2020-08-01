import React from 'react';
import PropTypes from 'prop-types';
import MyChart from './myChart';


class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      email: '', threshold: '2', isInput: false, highchartUrl: '/api/v1/d/' , input:'150', mychart:'',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);

    this.onInputSubmit = this.onInputSubmit.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    const { threshold, isInput } = this.state;




    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(() => ({
          threshold,
          isInput,
          email,
          threshold,
          IBMstock,
          highchartUrl: data.highchartUrl,
        }));
      })
      .catch((error) => console.log(error));
  }

  // eslint-disable-next-line react/sort-comp
  handleEmailChange(event) {
    this.setState({
      email: event.target.value,
    });
  }
  
  handleInputChange(event) {
    this.setState({
      input: event.target.value,
    });
  }

  handleChange(event) {
    this.setState({
      threshold: event.target.value,
    });
  }

  handleStockChange(event) {
    this.setState({
      IBMstock: event.target.value,
    });
  }

  onFormSubmit(event) {
    event.preventDefault();
    const { url } = this.props;
    const { email, threshold, highchartUrl,input } = this.state;
    fetch(url,
      {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'email': email, 'threshold': threshold,'url' : window.location.href,'input':input }),
        credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(() => {
        this.setState({
          email,
          threshold,
          isInput: true,
          anomaly,
          IBMstock,
          highchartUrl,
        });
      })
      .catch((error) => console.log(error));
  }

  onInputSubmit() {
    event.preventDefault();
    const { email, threshold, highchartUrl,input } = this.state;
    fetch("/api/v1/i/",
      {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'email': email, 'threshold': threshold,'url' : window.location.href,'input':input }),
        credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(() => {
        this.setState({
          email,
          threshold,
          isInput: true,
          highchartUrl,
        });
        window.location.reload();

      })
      .catch((error) => console.log(error));
  }

  render() {
    const {
      email, threshold, isInput, highchartUrl,input,
    } = this.state;
  
    var local_arr= window.location.href.split('/');
    var dataset=local_arr[local_arr.length - 1];

    if(dataset==='StockInput' || dataset==='StockInput?'){

      return (
        <div>
            <form onSubmit={this.onInputSubmit}>
              <table>
                <tr>

                  <td>Enter email address for alerting messages: </td>
                  <td>
                    <input type="text" value={email} onChange={this.handleEmailChange} />
                  </td>

                  <td>Customize threshold (1 to 3): </td>
                  <td>
                    <input type="number" value={threshold} min="1" max="3" step="0.1" onChange={this.handleChange} />
                  </td>


                  <td>Input new data: </td>
                  <td>
                    <input type="number" value={input} step="1" onChange={this.handleInputChange} />
                  </td>

                  <td>
                    <input type="submit" />
                  </td>
  
                </tr>
              </table>
            </form>        
          <MyChart url={highchartUrl} />
        </div>
      );
    }

    if (!isInput) {
      return (
        <div className="index">
          <form onSubmit={this.onFormSubmit}>
            <table>
              <tr>

                <td>Enter email address for alerting messages: </td>
                <td>
                  <input type="text" value={email} onChange={this.handleEmailChange} />
                </td>

                <td>Customize threshold (1 to 3): </td>
                  <td>
                    <input type="number" value={threshold} min="1" max="3" step="0.1" onChange={this.handleChange} />
                </td>

                <td>New IBM stock price </td>
                <td>
                  <input type="number" value={IBMstock} onChange={this.handleStockChange} />
                </td>


                <td>
                  <input type="submit" />
                </td>

              </tr>
            </table>
          </form>
        </div>
      );
    }


    return (
      <div>
        <MyChart url={highchartUrl} />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
