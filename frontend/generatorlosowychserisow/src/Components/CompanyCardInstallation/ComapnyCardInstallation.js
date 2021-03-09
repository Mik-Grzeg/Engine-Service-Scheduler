import React, { useState } from "react";
import { connect } from "react-redux";
import { makeStyles } from "@material-ui/core/styles";
import clsx from "clsx";
import Typography from "@material-ui/core/Typography";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { MdExpandMore, MdMoreVert } from "react-icons/md";
import PropTypes from "prop-types";

const useStyles = makeStyles((theme) => ({
  expand: {
    transform: "rotate(0deg)",
    marginLeft: "auto",
    transition: theme.transitions.create("transform", {
      duration: theme.transitions.duration.shortest,
    }),
  },
  expandOpen: {
    transform: "rotate(180deg)",
  },
}));

export const ComapnyCardInstallation = ({ installation }) => {
  console.log(installation);
  if (installation.engine === null) {
    installation = {
      ...installation,
      engine: {
        isThereEngine: false,
        enabled: "NO DATA",
        id: "NO ID",
        serial_number: "NO SERIAL NUMBER",
        type: "NO TYPE",
        message: " NO ENGINE CONNECTED TO INSTALATION",
      },
    };
  }
  if (typeof installation.contract_set === "undifiend") {
    installation = {
      ...installation,
      contract_set: [],
    };
  }

  const classes = useStyles();
  // Menu Stuff
  // MENU POSITION CHECK
  const handleClickMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  // Close Menu
  const handleCloseMenu = () => {
    setAnchorEl(null);
  };
  const [anchorEl, setAnchorEl] = useState(null);

  // More Info
  // Open More info
  const handleExpandClickMoreInfo = () => {
    setExpanded(!expanded);
  };
  const [expanded, setExpanded] = useState(false);

  return (
    <Card className={classes.root}>
      <CardHeader
        action={
          <>
            <IconButton aria-label="more options" onClick={handleClickMenu}>
              <MdMoreVert />
            </IconButton>
            <Menu
              id="simple-menu"
              anchorEl={anchorEl}
              keepMounted
              open={Boolean(anchorEl)}
              onClose={handleCloseMenu}
            >
              <MenuItem onClick={handleCloseMenu}>Edit</MenuItem>
              <MenuItem onClick={handleCloseMenu}>Delete</MenuItem>
            </Menu>
          </>
        }
        title={installation.installation_name}
        subheader={installation.installation_location}
      />
      <CardActions disableSpacing>
        <IconButton
          className={clsx(classes.expand, {
            [classes.expandOpen]: expanded,
          })}
          onClick={handleExpandClickMoreInfo}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <MdExpandMore />
        </IconButton>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Typography variant="h6">Engine</Typography>
          <Typography variant="body1">
            {installation.engine.id !== "NO ID" ? (
              <>
                Enabled : {installation.engine.enabled ? "ON" : "OFF"}
                <br />
                {!installation.engine.enabled && (
                  <>
                    Dissabled Till : {installation.engine.stopped_till} <br />
                  </>
                )}
                Serial number : {installation.engine.serial_number}
                <br />
                Type : {installation.engine.type}
              </>
            ) : (
              <> No Engine Connected </>
            )}
          </Typography>
          <Typography variant="h6">Contracts</Typography>
          <Typography variant="body1">
            {installation.contract_set.length !== 0 ? (
              installation.contract_set.map((contract) => {
                return (
                  <span key={contract.id}>
                    Start : {contract.contract_start}
                    <br />
                    Stop : {contract.contract_end}
                    <br />
                    <br />
                  </span>
                );
              })
            ) : (
              <>No contracts conneded to this installation</>
            )}
          </Typography>
        </CardContent>
      </Collapse>
    </Card>
  );
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = {};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ComapnyCardInstallation);
