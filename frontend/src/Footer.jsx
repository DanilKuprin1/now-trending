import React from "react";
import { Box, Typography, Link, IconButton, Stack } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import TwitterIcon from "@mui/icons-material/Twitter";

export default function Footer() {
  return (
    <Box
      sx={{
        bgcolor: "background.paper", // ← matches your theme’s dark blue-gray
        color: "text.primary", // ← ensures high contrast for text
        py: 6,
        mt: 10,
      }}
    >
      <Box maxWidth="lg" mx="auto" px={3}>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          spacing={4}
          justifyContent="space-between"
          alignItems={{ xs: "flex-start", sm: "center" }}
        >
          <Box>
            <Typography variant="h6" color="common.white">
              Now-Trending.world
            </Typography>
            <Typography variant="body2" sx={{ mt: 1 }}>
              Built with React + MUI + ☕
            </Typography>
          </Box>

          <Box>
            {/* <Typography variant="body2" sx={{ mb: 1 }}>
              Check out the source:
            </Typography>
            <Link
              href="https://github.com/yourusername/yourproject"
              target="_blank"
              rel="noopener"
              underline="hover"
              color="primary.light"
            >
              github.com/yourusername/yourproject
            </Link> */}
          </Box>
          <Stack direction="row" spacing={1}>
            <IconButton
              href="https://github.com/DanilKuprin1"
              target="_blank"
              rel="noopener"
              color="inherit"
            >
              <GitHubIcon />
            </IconButton>
            <IconButton
              href="https://www.linkedin.com/in/danilkuprin1/"
              target="_blank"
              rel="noopener"
              color="inherit"
            >
              <LinkedInIcon />
            </IconButton>
            <IconButton href="" target="_blank" rel="noopener" color="inherit">
              <TwitterIcon />
            </IconButton>
          </Stack>
        </Stack>
        <Box mt={4} textAlign="center">
          <Typography variant="caption" color="grey.500">
            © {new Date().getFullYear()} Danil Kuprin — All rights reserved.
          </Typography>
          <Typography variant="caption" color="grey.600" display="block" mt={1}>
            You’ve reached the end of the DOM. Time to git push your dreams. 🚀
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
