FROM python:3.12
EXPOSE 8080

# Install pipx
RUN python -m pip install --upgrade pip
RUN python -m pip install pipx
RUN pipx ensurepath

# Add pipx binary path to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install mitmproxy using pipx
RUN pipx install mitmproxy
RUN mitmproxy --version

# Install elasticsearch using pipx
RUN pipx inject mitmproxy elasticsearch

# Copy gwm-ghc-dev.py to gwm-ghc.py
WORKDIR /ghcscript
COPY gwm-ghc-dev.py gwm-ghc.py

# Set the entrypoint to mitmdump with the script
ENTRYPOINT ["mitmdump", "-s", "gwm-ghc.py"]
# CMD ["python"]