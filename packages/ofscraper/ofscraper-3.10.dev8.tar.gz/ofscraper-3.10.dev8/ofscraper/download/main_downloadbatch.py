r"""
                                                             
 _______  _______         _______  _______  _______  _______  _______  _______  _______ 
(  ___  )(  ____ \       (  ____ \(  ____ \(  ____ )(  ___  )(  ____ )(  ____ \(  ____ )
| (   ) || (    \/       | (    \/| (    \/| (    )|| (   ) || (    )|| (    \/| (    )|
| |   | || (__     _____ | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
| |   | ||  __)   (_____)(_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
| |   | || (                   ) || |      | (\ (   | (   ) || (      | (      | (\ (   
| (___) || )             /\____) || (____/\| ) \ \__| )   ( || )      | (____/\| ) \ \__
(_______)|/              \_______)(_______/|/   \__/|/     \||/       (_______/|/   \__/
                                                                                      
"""

import asyncio
import pathlib
import traceback
from functools import partial

import aiofiles

try:
    from win32_setctime import setctime  # pylint: disable=import-error
except ModuleNotFoundError:
    pass
import ofscraper.classes.placeholder as placeholder
import ofscraper.download.shared.general as common
import ofscraper.download.shared.globals.globals as common_globals
import ofscraper.utils.cache as cache
import ofscraper.utils.constants as constants
import ofscraper.utils.live.screens as progress_utils
import ofscraper.utils.system.system as system
from ofscraper.download.shared.classes.retries import download_retry
from ofscraper.download.shared.general import (
    check_forced_skip,
    downloadspace,
    get_data,
    get_medialog,
    get_resume_size,
    get_unknown_content_type,
    size_checker,
)
from ofscraper.download.shared.progress.chunk import (
    get_ideal_chunk_size,
    get_update_count,
)
from ofscraper.download.shared.handle_result import handle_result_main
from ofscraper.download.shared.log import get_url_log, path_to_file_logger
from ofscraper.download.shared.metadata import force_download

from ofscraper.download.shared.send.send_bar_msg import (
    send_bar_msg_batch
)


async def main_download(c, ele, username, model_id):
    common_globals.innerlog.get().debug(
        f"{get_medialog(ele)} Downloading with normal batch downloader"
    )
    common_globals.innerlog.get().debug(
        f"{get_medialog(ele)} download url: {get_url_log(ele)}"
    )
    if common.is_bad_url(ele.url):
        common_globals.log.debug(
            f"{get_medialog(ele)} Forcing download because known bad url"
        )
        await force_download(ele, username, model_id)
        return ele.mediatype, 0

    result = list(await main_download_downloader(c, ele))
    if result[0] == 0:
        if ele.mediatype != "forced_skipped":
            await force_download(ele, username, model_id)
        return ele.mediatype, 0
    return await handle_result_main(result, ele, username, model_id)


async def main_download_downloader(c, ele):
    downloadspace(mediatype=ele.mediatype)
    tempholderObj = await placeholder.tempFilePlaceholder(
        ele, f"{await ele.final_filename}_{ele.id}.part"
    ).init()
    async for _ in download_retry():
        with _:
            try:
                common_globals.attempt.set(common_globals.attempt.get(0) + 1)
                (
                    pathlib.Path(tempholderObj.tempfilepath).unlink(missing_ok=True)
                    if common_globals.attempt.get() > 1
                    else None
                )
                data = await get_data(ele)
                if data:
                    return await resume_data_handler(data, c, ele, tempholderObj)
                else:
                    return await fresh_data_handler(c, ele, tempholderObj)

            except OSError as E:
                common_globals.innerlog.get().debug(
                    f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] Number of open Files across all processes-> {len(system.getOpenFiles(unique=False))}"
                )
                common_globals.innerlog.get().debug(
                    f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] Number of unique open files across all processes-> {len(system.getOpenFiles())}"
                )
                common_globals.innerlog.get().debug(
                    f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] Unique files data across all process -> {list(map(lambda x:(x.path,x.fd),(system.getOpenFiles())))}"
                )
                raise E
            except Exception as E:
                common_globals.innerlog.get().traceback_(
                    f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] {traceback.format_exc()}"
                )
                common_globals.innerlog.get().traceback_(
                    f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] {E}"
                )
                common_globals.log.handlers[1].queue.put(
                list(common_globals.innerlog.get().handlers[1].queue.queue)
                )
                common_globals.log.handlers[0].queue.put(
                list(common_globals.innerlog.get().handlers[0].queue.queue)
                )
                raise E


async def fresh_data_handler(c, ele, tempholderObj):
    result = None
    try:
        result = await main_download_sendreq(
            c, ele, tempholderObj, placeholderObj=None, total=None
        )
    except Exception as E:
        raise E
    return result


async def resume_data_handler(data, c, ele, tempholderObj):
    common_globals.log.debug(f"{get_medialog(ele)} Resume cached data {data}")
    content_type = data.get("content-type").split("/")[-1]
    total = int(data.get("content-total")) if data.get("content-total") else None
    placeholderObj = await placeholder.Placeholders(ele, content_type).init()
    resume_size = get_resume_size(tempholderObj, mediatype=ele.mediatype)
    common_globals.log.debug(f"{get_medialog(ele)} resume_size: {resume_size}  and total: {total}")

    # other
    if await check_forced_skip(ele, total) == 0:
        path_to_file_logger(placeholderObj, ele, common_globals.innerlog.get())
        return (
            0,
            tempholderObj.tempfilepath,
            placeholderObj,
        )
    elif total == resume_size:
        common_globals.log.debug(f"{get_medialog(ele)} total==resume_size skipping download")
        path_to_file_logger(placeholderObj, ele, common_globals.innerlog.get())
        (
            await common.batch_total_change_helper(None, total)
            if common_globals.attempt.get() == 1
            else None
        )
        return (
            total,
            tempholderObj.tempfilepath,
            placeholderObj,
        )

    else:
        try:
            return await main_download_sendreq(
                c, ele, tempholderObj, total=total, placeholderObj=placeholderObj
            )
        except Exception as E:
            raise E


async def main_download_sendreq(c, ele, tempholderObj, placeholderObj=None, total=None):
    try:
        common_globals.innerlog.get().debug(
            f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] download temp path {tempholderObj.tempfilepath}"
        )
        return await send_req_inner(
            c, ele, tempholderObj, placeholderObj=placeholderObj, total=total
        )
    except OSError as E:
        raise E
    except Exception as E:
        raise E


async def send_req_inner(c, ele, tempholderObj, placeholderObj=None, total=None):
    try:
        common_globals.log.debug(f"{get_medialog(ele)} writing item to disk")

        resume_size = get_resume_size(tempholderObj, mediatype=ele.mediatype)
        headers = None if not resume_size else {"Range": f"bytes={resume_size}-"}
        common_globals.log.debug(
            f"{get_medialog(ele)} [attempt {common_globals.attempt.get()}/{constants.getattr('DOWNLOAD_FILE_NUM_TRIES')}] Downloading media with url {ele.url}"
        )
        async with c.requests_async(url=ele.url, headers=headers) as r:
            total = total or int(r.headers["content-length"])
            await common.batch_total_change_helper(None, total)
            await asyncio.get_event_loop().run_in_executor(
                common_globals.thread,
                partial(
                    cache.set,
                    f"{ele.id}_headers",
                    {
                        "content-total": total,
                        "content-type": r.headers.get("content-type"),
                    },
                ),
            )
            content_type = r.headers.get("content-type").split("/")[
                -1
            ] or get_unknown_content_type(ele)
            if not placeholderObj:
                placeholderObj = await placeholder.Placeholders(
                    ele, content_type
                ).init()
            path_to_file_logger(placeholderObj, ele, common_globals.innerlog.get())
            if await check_forced_skip(ele, total) == 0:
                total = 0
                await common.batch_total_change_helper(total, 0)
            elif total != resume_size:
                await download_fileobject_writer(
                    r, ele, total, tempholderObj, placeholderObj
                )
        await size_checker(tempholderObj.tempfilepath, ele, total)
        return (total, tempholderObj.tempfilepath, placeholderObj)
    except Exception as E:
        await common.batch_total_change_helper(total, 0)
        raise E


async def download_fileobject_writer(r, ele, total, tempholderObj, placeholderObj):
    pathstr = str(placeholderObj.trunicated_filepath)
    try:
        await common.send_msg(
            partial(
                progress_utils.add_download_job_multi_task,
                f"{(pathstr[:constants.getattr('PATH_STR_MAX')] + '....') if len(pathstr) > constants.getattr('PATH_STR_MAX') else pathstr}\n",
                ele.id,
                total=total,
            )
        )

        fileobject = await aiofiles.open(tempholderObj.tempfilepath, "ab").__aenter__()
        download_sleep = constants.getattr("DOWNLOAD_SLEEP")

        await common.send_msg(
            partial(progress_utils.update_download_multi_job_task, ele.id, visible=True)
        )
        chunk_size = get_ideal_chunk_size(total, tempholderObj.tempfilepath)
        update_count = get_update_count(total, tempholderObj.tempfilepath, chunk_size)

        count = 1
        async for chunk in r.iter_chunked(chunk_size):
            common_globals.innerlog.get().trace(
                f"{get_medialog(ele)} Download Progress:{(pathlib.Path(tempholderObj.tempfilepath).absolute().stat().st_size)}/{total}"
            )
            await fileobject.write(chunk)
            await send_bar_msg_batch(
                    partial(
                        progress_utils.update_download_multi_job_task,
                        ele.id,
                        completed=pathlib.Path(tempholderObj.tempfilepath)
                        .absolute()
                        .stat()
                        .st_size,
                    ),count,update_count
            )
            count += 1
            (await asyncio.sleep(download_sleep)) if download_sleep else None
    except Exception as E:
        # reset download data
        raise E
    finally:
        try:
            await common.send_msg(
                partial(progress_utils.remove_download_multi_job_task, ele.id)
            )
        except:
            None

        try:
            await fileobject.close()
        except Exception:
            None
