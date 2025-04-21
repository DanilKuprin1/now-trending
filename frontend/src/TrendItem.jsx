import {
  CircularProgress,
  Typography,
  Box,
  Button,
  List,
  LinearProgress,
} from "@mui/material";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

import Post from "./Post";

import * as React from "react";
import GlowWrapper from "./GlowWrapper";

export default function TrendItem({ name, post }) {
  if (!name) {
    return <CircularProgress />;
  }
  return (
    <Box sx={{ justifyContent: "center" }}>
      <Typography
        variant="h4"
        sx={{
          fontWeight: "bold",
          textAlign: "center",
          color: "#ffffff",
          textShadow: "0 2px 8px rgba(0,0,0,0.6)",
          letterSpacing: 1.5,
          mb: 2,
        }}
      >
        {name}
      </Typography>

      {!post ? (
        <Box display="flex" justifyContent="center" alignItems="center" px={2}>
          <LinearProgress sx={{ width: "100%" }} />
        </Box>
      ) : (
        <>
          <Box display={"block"}>
            <GlowWrapper objectToTrack={post} display="block">
              <Post
                userName={post.name}
                userSceenName={post.screen_name}
                avatarUrl={post.avatar}
                createdAt={post.created_at}
                text={post.text}
                favorites={post.favorites}
                replies={post.replies}
                retweets={post.retweets}
                views={post.views}
                media={post.media}
              ></Post>
            </GlowWrapper>
          </Box>

          <Button
            href={post.source}
            variant="text"
            size="small"
            endIcon={<OpenInNewIcon sx={{ fontSize: 16, mt: "-1px" }} />}
            sx={{
              color: "#1d9bf0",
              fontSize: 14,
              pl: 2,
            }}
          >
            View original post
          </Button>
        </>
      )}
    </Box>
  );
}
