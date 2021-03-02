import react, { useEffect } from "react";
import { connect } from "react-redux";
import { autoLogin } from "./actions/userActions";
import LoginContainer from "./containers/LoginContainer";
import MainContainer from "./containers/MainContainer";

function App({ loggedIn, name, autoLogin }) {
  useEffect(() => {
    autoLogin();
  }, []);
  return <>{!loggedIn ? <LoginContainer /> : <MainContainer />}</>;
}

const mapStateToProps = (state) => {
  return {
    loggedIn: state.userReducer.loggedIn,
    name: state.userReducer.user.name,
  };
};
const mapDispatchToState = (dispatch) => {
  return {
    autoLogin: () => dispatch(autoLogin()),
  };
};

export default connect(mapStateToProps, mapDispatchToState)(App);
