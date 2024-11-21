#!/bin/bash

sudo rm -rf /usr/local/go &&
cd &&
wget https://dl.google.com/go/go1.23.0.linux-amd64.tar.gz &&
sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz &&
export PATH=$PATH:/usr/local/go/bin &&
go install golang.org/x/lint/golint@latest &&
export PATH=$PATH:$(go env GOPATH)/bin &&
sudo apt install -y \
golang-github-rs-xid-dev golang-github-rs-zerolog-dev golang-github-rsc-devweb \
golang-github-rubenv-sql-migrate-dev golang-github-rubyist-tracerx-dev \
golang-github-russellhaering-goxmldsig-dev golang-github-russross-blackfriday-dev \
golang-github-russross-blackfriday-v2-dev golang-github-ruudk-golang-pdf417-dev \
golang-github-rwcarlsen-goexif-dev golang-github-ryanuber-columnize-dev \
golang-github-ryanuber-go-glob-dev golang-github-ryszard-goskiplist-dev \
golang-github-sabhiram-go-gitignore-dev golang-github-safchain-ethtool-dev \
golang-github-sahilm-fuzzy-dev golang-github-samalba-dockerclient-dev \
golang-github-samuel-go-zookeeper-dev golang-github-sanity-io-litter-dev \
golang-github-sap-go-hdb-dev golang-github-saracen-walker-dev \
golang-github-sasha-s-go-deadlock-dev golang-github-satori-go.uuid-dev \
golang-github-satta-ifplugo-dev golang-github-schollz-closestmatch-dev \
golang-github-schollz-progressbar-dev golang-github-scylladb-termtables-dev \
golang-github-sean--pager-dev golang-github-sean--seed-dev \
golang-github-seandolphin-bqschema-dev golang-github-sebdah-goldie-dev \
golang-github-sebest-xff golang-github-sebest-xff-dev \
golang-github-seccomp-containers-golang-dev golang-github-seccomp-libseccomp-golang-dev \
golang-github-segmentio-fasthash-dev golang-github-segmentio-kafka-go-dev \
golang-github-segmentio-ksuid-dev golang-github-seiflotfy-cuckoofilter-dev \
golang-github-serenize-snaker-dev golang-github-sergi-go-diff-dev \
golang-github-sethvargo-go-fastly-dev golang-github-sevlyar-go-daemon-dev \
golang-github-shenwei356-bio-dev golang-github-shenwei356-bpool-dev \
golang-github-shenwei356-breader-dev golang-github-shenwei356-bwt-dev \
golang-github-shenwei356-natsort-dev golang-github-shenwei356-util-dev \
golang-github-shenwei356-xopen-dev golang-github-shibukawa-configdir-dev \
golang-github-shiena-ansicolor-dev golang-github-shirou-gopsutil-dev \
golang-github-shogo82148-go-shuffle-dev golang-github-shopify-logrus-bugsnag-dev \
golang-github-shopify-sarama-dev golang-github-shopspring-decimal-dev \
golang-github-showmax-go-fqdn-dev golang-github-shurcool-githubv4-dev \
golang-github-shurcool-gopherjslib-dev golang-github-shurcool-graphql-dev \
golang-github-shurcool-httpfs-dev golang-github-shurcool-httpgzip-dev \
golang-github-shurcool-sanitized-anchor-name-dev golang-github-siddontang-go-dev \
golang-github-siddontang-go-snappy-dev golang-github-siddontang-goredis-dev \
golang-github-siddontang-rdb-dev golang-github-sirupsen-logrus-dev \
golang-github-sjoerdsimons-ostree-go-dev golang-github-skarademir-naturalsort-dev \
golang-github-skeema-mybase-dev golang-github-skip2-go-qrcode-dev \
golang-github-skratchdot-open-golang-dev golang-github-smallfish-simpleyaml-dev \
golang-github-smallstep-assert-dev golang-github-smallstep-cli-dev \
golang-github-smallstep-nosql-dev golang-github-smallstep-truststore-dev \
golang-github-smartystreets-assertions-dev golang-github-smartystreets-go-aws-auth-dev \
golang-github-smartystreets-goconvey-dev golang-github-smartystreets-gunit-dev \
golang-github-smira-commander-dev golang-github-smira-flag-dev \
golang-github-smira-go-aws-auth-dev golang-github-smira-go-ftp-protocol-dev \
golang-github-smira-go-xz-dev golang-github-snapcore-snapd-dev \
golang-github-socketplane-libovsdb-dev golang-github-soheilhy-cmux-dev \
golang-github-soniah-dnsmadeeasy-dev golang-github-soundcloud-go-runit-dev \
golang-github-sourcegraph-jsonrpc2-dev golang-github-spacejam-loghisto-dev \
golang-github-spaolacci-murmur3-dev golang-github-spf13-afero-dev \
golang-github-spf13-cast-dev golang-github-spf13-cobra-dev \
golang-github-spf13-fsync-dev golang-github-spf13-jwalterweatherman-dev \
golang-github-spf13-nitro-dev golang-github-spf13-pflag-dev \
golang-github-spf13-viper-dev golang-github-spkg-bom-dev \
golang-github-src-d-gcfg-dev golang-github-ssgelm-cookiejarparser-dev \
golang-github-ssor-bom-dev golang-github-stacktic-dropbox-dev \
golang-github-stathat-go-dev golang-github-steveyen-gtreap-dev \
golang-github-stevvooe-resumable-dev golang-github-stoewer-go-strcase-dev \
golang-github-streadway-amqp-dev golang-github-stretchr-objx-dev \
golang-github-stretchr-testify-dev golang-github-stvp-go-udp-testing-dev \
golang-github-stvp-roll-dev golang-github-stvp-tempredis-dev \
golang-github-suapapa-go-eddystone-dev golang-github-subosito-gotenv-dev \
golang-github-surma-gocpio-dev golang-github-svanharmelen-jsonapi-dev \
golang-github-svent-go-flags-dev golang-github-svent-go-nbreader-dev \
golang-github-sylabs-json-resp-dev golang-github-sylabs-sif-dev \
golang-github-syncthing-notify-dev golang-github-syncthing-syncthing-dev \
golang-github-syndtr-goleveldb-dev golang-github-tarm-serial-dev \
golang-github-tatsushid-go-prettytable-dev golang-github-tchap-go-patricia-dev \
golang-github-tcnksm-go-gitconfig-dev golang-github-tdewolff-minify-dev \
golang-github-tdewolff-parse-dev golang-github-tdewolff-test-dev \
golang-github-tealeg-xlsx-dev golang-github-teambition-rrule-go-dev \
golang-github-templexxx-cpufeat-dev golang-github-templexxx-reedsolomon-dev \
golang-github-templexxx-xor-dev golang-github-tent-canonical-json-go-dev \
golang-github-tent-http-link-go-dev golang-github-teris-io-shortid-dev \
golang-github-terra-farm-udnssdk-dev golang-github-tevino-abool-dev \
golang-github-thales-e-security-pool-dev golang-github-thalesignite-crypto11-dev \
golang-github-thcyron-uiprogress-dev golang-github-thecreeper-go-notify-dev \
golang-github-thedevsaddam-gojsonq-dev golang-github-thejerf-suture-dev \
golang-github-thoj-go-ircevent-dev golang-github-thomasrooney-gexpect-dev \
golang-github-thomsonreuterseikon-go-ntlm-dev golang-github-throttled-throttled-dev \
golang-github-tideland-golib-dev golang-github-tidwall-btree-dev \
golang-github-tidwall-buntdb-dev golang-github-tidwall-gjson-dev \
golang-github-tidwall-grect-dev golang-github-tidwall-match-dev \
golang-github-tidwall-pretty-dev golang-github-tidwall-rtree-dev \
golang-github-tidwall-tinyqueue-dev golang-github-timberio-go-datemath-dev \
golang-github-tinylib-msgp-dev golang-github-tjfoc-gmsm-dev \
golang-github-tklauser-go-sysconf-dev golang-github-tklauser-numcpus-dev \
golang-github-tmc-grpc-websocket-proxy-dev golang-github-tmc-scp-dev \
golang-github-tobi-airbrake-go-dev golang-github-tombuildsstuff-giovanni-dev \
golang-github-tomnomnom-linkheader-dev golang-github-tonistiigi-fifo-dev \
golang-github-tonistiigi-fsutil-dev golang-github-tonistiigi-units-dev \
golang-github-toqueteos-webbrowser-dev golang-github-traefik-yaegi-dev \
golang-github-tsenart-tb-dev golang-github-ttacon-chalk-dev \
golang-github-tv42-httpunix-dev golang-github-twinj-uuid-dev \
golang-github-twmb-murmur3-dev && go mod init new
