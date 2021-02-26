import react, { useEffect } from "react";
import { connect } from "react-redux";
import { LOG_IN, AUTO_LOG_IN } from "./actions/userActions";
import LoginContainer from "./containers/LoginContainer";

function App({ loggedIn }) {
  useEffect(() => {
    console.log(loggedIn);
  }, []);
  return <>{!loggedIn ? <LoginContainer /> : <div>nie zalogowany</div>}</>;
}

const mapStateToProps = (state) => {
  return { loggedIn: state.loggedIn };
};
const mapDispatchToState = (dispatch) => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToState)(App);
