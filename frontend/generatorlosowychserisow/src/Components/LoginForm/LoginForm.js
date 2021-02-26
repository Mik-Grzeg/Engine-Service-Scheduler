import React, { useState } from "react";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import InputAdornment from "@material-ui/core/InputAdornment";
import IconButton from "@material-ui/core/IconButton";
import Input from "@material-ui/core/Input";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import { connect } from "react-redux";
import { MdVisibility } from "react-icons/md";
import { MdVisibilityOff } from "react-icons/md";
import "./LoginForm.scss";

function LoginForm({ requierdEmail }) {
  const [values, setValues] = useState({
    email: "",
    password: "",
    showPassword: false,
  });

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
  };

  const handleClickShowPassword = () => {
    setValues({ ...values, showPassword: !values.showPassword });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (values.email.includes(requierdEmail)) {
      //Post if data is correct
    } else if (!values.email.includes("@")) {
      //if the email value doesnt contein @ we
      //suppose user added only the beggining of his email
      setValues({
        ...values,
        email: values.email.concat(requierdEmail),
      });
    }
  };

  return (
    <>
      <Grid container direction="row" justify="center" spacing={4}>
        <Grid item xs={12} className="login_logo"></Grid>
        <Grid className="EmailMargin" item xs={12} sm={10} md={8}>
          <FormControl fullWidth={true}>
            <InputLabel htmlFor="email">Email</InputLabel>
            <Input
              id="email"
              type="email"
              value={values.email}
              onChange={handleChange("email")}
              endAdornment={
                <InputAdornment position="end">{requierdEmail}</InputAdornment>
              }
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={10} md={8}>
          <FormControl fullWidth={true}>
            <InputLabel htmlFor="password">Password</InputLabel>
            <Input
              id="password"
              type={values.showPassword ? "text" : "password"}
              value={values.password}
              onChange={handleChange("password")}
              endAdornment={
                <InputAdornment>
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={handleClickShowPassword}
                  >
                    {values.showPassword ? (
                      <MdVisibility />
                    ) : (
                      <MdVisibilityOff />
                    )}
                  </IconButton>
                </InputAdornment>
              }
            />
          </FormControl>
        </Grid>
      </Grid>
      <Grid container justify="center" spacing={6}>
        <Grid item>
          <Button
            variant="contained"
            color="primary"
            type="submit"
            onClick={handleSubmit}
          >
            Zaloguj sie
          </Button>
        </Grid>
      </Grid>
    </>
  );
}

const mapStateToProps = (state) => {
  return { requierdEmail: state.requierdEmail };
};

export default connect(mapStateToProps)(LoginForm);
