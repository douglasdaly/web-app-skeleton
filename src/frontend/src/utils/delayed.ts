// Javier on StackOverflow: https://stackoverflow.com/a/60600274
export class CancelablePromise<T> extends Promise<T> {
  private onCancel: () => void

  constructor(executor: (resolve: (value?: T | PromiseLike<T>) => void, reject: (reason?: any) => void, onCancel: (cancelHandler: () => void) => void) => void) {
    let onCancel: () => void;
    super((rs, rj) => executor(rs, rj, (ch: () => void) => onCancel = ch));
    // @ts-ignore: Gets set upon super() call.
    this.onCancel = onCancel;
  }

  public cancel() {
    if (this.onCancel) {
      this.onCancel();
    }
  }
}

export function delayCall<T>(delay: number, callback: (...args: any[]) => T, ...args: any[]): CancelablePromise<T> {
  return new CancelablePromise((resolve, reject, onCancel) => {
    const id = setTimeout(() => resolve(callback(...args)), delay);
    onCancel(() => {
      clearTimeout(id);
    });
  });
};

export default {
  CancelablePromise,
  delayCall,
};
