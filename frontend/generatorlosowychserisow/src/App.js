import react, { useEffect } from "react";
import { connect } from "react-redux";
import { LOG_IN, AUTO_LOG_IN } from "./actions/userActions";
import LoginContainer from "./containers/LoginContainer";
import MainContainer from "./containers/MainContainer";

function App({ loggedIn, name }) {
  useEffect(() => {}, []);
  return <>{!loggedIn ? <LoginContainer /> : <MainContainer />}</>;
}

const mapStateToProps = (state) => {
  return {
    loggedIn: state.userReducer.loggedIn,
    name: state.userReducer.user.name,
  };
};
const mapDispatchToState = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToState)(App);
