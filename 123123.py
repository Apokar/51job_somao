from multiprocessing import Pool

main_urls=[]

def get_main_url(i):
    for c in range(1, 7):
        for d in range(1, 8):
            for a in range(1, 12):
                if a < 10:
                    main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + '0' + str(
                            a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                            i) + '&cotype=99&degreefrom=' + '0' + str(
                            c) + '&jobterm=99&companysize=' + '0' + str(
                            d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')

                else:
                    main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + str(
                            a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                            i) + '&cotype=99&degreefrom=' + '0' + str(
                            c) + '&jobterm=99&companysize=' + '0' + str(
                            d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
    return main_urls

def main(i):
    get_main_url(i)
    print len(main_urls)

if __name__=='__main__':
    pool = Pool(4)

    pool.map(main, [i for i in range(1, 7)])
    pool.close()
    pool.join()