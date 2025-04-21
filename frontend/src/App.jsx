import Box from "@mui/material/Box";
import AppBar from "@mui/material/AppBar";
import Typography from "@mui/material/Typography";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline, Toolbar } from "@mui/material";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import * as React from "react";

import useScrollTrigger from "@mui/material/useScrollTrigger";

import Slide from "@mui/material/Slide";

import TrendsList from "./TrendsList.jsx";
import Footer from "./Footer.jsx";

function App() {
  const trigger = useScrollTrigger();
  const theme = createTheme({
    palette: {
      mode: "dark",
      primary: {
        main: "#1DA1F2",
      },
      secondary: {
        main: "#141D26",
      },
      success: {
        main: "#17BF63",
      },
      error: {
        main: "#E0245E",
      },
      warning: {
        main: "#FFAD1F",
      },
      info: {
        main: "#00C2FF",
      },
      background: {
        default: "#141D26",
        paper: "#1B2836",
      },
      text: {
        primary: "#E6ECF0",
        secondary: "#8899A6",
      },
    },
    shape: {
      borderRadius: 20,
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> {}
      <Box
        sx={{
          width: "100%",
          maxWidth: "100vw",
          overflowX: "hidden",
          boxSizing: "border-box",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignContent: "center",
          justifyContent: "center",
        }}
      >
        <Slide appear={false} direction="down" in={!trigger}>
          <AppBar position="sticky" elevation={0}>
            <Toolbar sx={{ justifyContent: "center" }}>
              <Typography variant="h5" component={"h1"} color="text.primary">
                Now-Trending 👀
              </Typography>
            </Toolbar>
          </AppBar>
        </Slide>
        <Box
          display="flex"
          justifyContent={"center"}
          flexDirection={"column"}
          alignContent={"center"}
          px={{ xs: 2, sm: 4, md: 6, lg: 8 }}
          pt={{ xs: 3, lg: 4 }}
        >
          <TrendsList sx={{ width: "100%" }}></TrendsList>
        </Box>
        <Box sx={{ mt: "auto " }}>
          <Footer></Footer>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
