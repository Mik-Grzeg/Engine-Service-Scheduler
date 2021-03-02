import React, { useState } from "react";
import { connect } from "react-redux";
//@MATERIAL UI COMPONENTS
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
//REACT ICONS
import { MdChevronLeft, MdMenu } from "react-icons/md";
import { BsFillCalendarFill } from "react-icons/bs";
import { GiFactory } from "react-icons/gi";
import { FaFileInvoiceDollar } from "react-icons/fa";
import { FiLogOut } from "react-icons/fi";
//CONTAINERS
import CompanyContainer from "./CompanyContainer";
//ACTIONS
import { logOut } from "../actions/userActions";
//STYTLING
import "./MainContainer.scss";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";

const drawerWidth = 220;
//important STUFF FROM MATERIAL UI
const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  hide: {
    display: "none",
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: "nowrap",
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerClose: {
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: "hidden",
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up("sm")]: {
      width: theme.spacing(9) + 1,
    },
  },
  toolbar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(0),
  },
  toolbartext: {
    flexGrow: 1,
  },
  icon: {
    fontSize: "1.6rem",
    marginLeft: "6px",
  },
  iconContainer: {
    maxWidth: "24px",
  },
  sectionDesktop: {
    display: "none",
    [theme.breakpoints.up("md")]: {
      display: "flex",
    },
  },
  sectionMobile: {
    display: "flex",
    [theme.breakpoints.up("md")]: {
      display: "none",
    },
  },
}));

const MainContainer = ({ userName = "", logOut }) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <div className={classes.root}>
      <AppBar
        position="fixed"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            className={clsx(classes.menuButton, {
              [classes.hide]: open,
            })}
          >
            <MdMenu />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            align="right"
            className={classes.toolbartext}
          >
            Welcome {userName}
            <Button
              color="default"
              endIcon={<FiLogOut />}
              onClick={() => {
                logOut();
              }}
            ></Button>
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
      >
        <div className={classes.toolbar}>
          <IconButton onClick={handleDrawerClose}>
            <MdChevronLeft />
          </IconButton>
        </div>
        <Divider />
        <List>
          <ListItem button>
            <ListItemIcon>
              <BsFillCalendarFill className={classes.icon} className="icon" />
            </ListItemIcon>
            <ListItemText primary={"Calendar"} />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <GiFactory className={classes.icon} className="icon" />
            </ListItemIcon>
            <ListItemText primary={"Company"} />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <FaFileInvoiceDollar className={classes.icon} className="icon" />
            </ListItemIcon>
            <ListItemText primary={"Budget"} />
          </ListItem>
        </List>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.toolbar} />
        <CompanyContainer />
      </main>
    </div>
  );
};

const mapStateToProps = (state) => {
  return {
    userName: state.userReducer.user.name,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    logOut: () => dispatch(logOut()),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(MainContainer);
