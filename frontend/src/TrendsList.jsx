import { Box, CircularProgress, Grid, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import ReconnectingWebSocket from "reconnecting-websocket";
import * as React from "react";
import TrendItem from "./TrendItem";

export default function TrendsList() {
  const [trends, setTrends] = useState([]);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new ReconnectingWebSocket(
      `${wsProtocol}://${import.meta.env.VITE_WS_DOMAIN}/ws`
    );
    socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      console.log("Received: ", message);

      if (message["message-type"] === "trends_list") {
        const trendNames = message["data"].map((trend) => trend.name);
        setTrends(trendNames);
      } else if (message["message-type"] === "trend_posts") {
        const { trend_id, post } = message["data"];
        setPosts((prev) => {
          const copy = [...prev];
          copy[trend_id] = post;
          return copy;
        });
      }
    });
    return () => socket.close();
  }, []);

  return (
    <Grid
      container
      columns={{ xs: 4, sm: 8, lg: 12 }}
      spacing={{ xs: 4, lg: 4 }}
    >
      {trends.length !== 0 ? (
        trends.map((trend, i) => {
          return (
            <Grid key={trend} size={4}>
              <Box
                sx={{
                  maxWidth: "540px",
                  width: "100%",
                  mx: "auto",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <TrendItem name={trend} post={posts[i]}></TrendItem>
              </Box>
            </Grid>
          );
        })
      ) : (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
            width: "100%",
          }}
        >
          <Typography pt={7} paddingBottom={6} variant="h5">
            Loading Trends...
          </Typography>
          <CircularProgress></CircularProgress>
        </Box>
      )}
    </Grid>
  );
}
